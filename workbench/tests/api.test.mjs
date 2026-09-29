import {test,after,before} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
const port=14319,base=`http://127.0.0.1:${port}`,root=path.resolve('..');let proc,tmp,admin,clientA,clientB,upload,initialReferenceCount;
async function req(url,body,cookie){const r=await fetch(base+url,{method:body?'POST':'GET',headers:{...(body?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},body:body?JSON.stringify(body):undefined});const d=await r.json();return {status:r.status,d,cookie:r.headers.get('set-cookie')?.split(';')[0]}}
async function startServer(){proc=spawn(process.execPath,['server.mjs'],{env:{...process.env,PORT:String(port),DALALA_DATA_DIR:tmp,DALALA_REGISTRY:path.join(tmp,'registry.json'),DALALA_CODEX_BIN:path.join(tmp,'fake-codex'),DALALA_TEST_CODEX_ARGS_FILE:path.join(tmp,'codex-args.txt'),DALALA_LOCAL_NO_LOGIN:'0',DALALA_SKIP_SEED:'1'},stdio:['ignore','pipe','pipe']});await new Promise((resolve,reject)=>{proc.stdout.once('data',resolve);proc.once('error',reject);proc.once('exit',()=>reject(Error('Server stopped')))});}
before(async()=>{tmp=await fs.mkdtemp(path.join(os.tmpdir(),'dalala-test-'));await fs.copyFile(path.join(root,'cover-skills/registry.json'),path.join(tmp,'registry.json'));initialReferenceCount=JSON.parse(await fs.readFile(path.join(tmp,'registry.json'),'utf8')).skills.length;await fs.writeFile(path.join(tmp,'fake-codex'),'#!/bin/sh\nprintf \'%s\\n\' "$@" > "$DALALA_TEST_CODEX_ARGS_FILE"\nexec sleep 30\n',{mode:0o755});await startServer()});
after(()=>proc?.kill());
test('unauthenticated API requires login',async()=>assert.equal((await req('/api/state')).status,401));
test('first account is admin; cannot claim admin twice',async()=>{admin=await req('/api/setup',{name:'Test owner',email:'owner@test.local',password:'test-pass-12345'});assert.equal(admin.d.user.role,'admin');assert.equal((await req('/api/setup',{email:'hijack@test.local',password:'test-pass-12345'})).status,400)});
test('customers cannot self-assign admin',async()=>{clientA=await req('/api/register',{email:'a@test.local',password:'test-pass-12345',role:'admin'});clientB=await req('/api/register',{email:'b@test.local',password:'test-pass-12345'});assert.equal(clientA.d.user.role,'client');assert.equal((await req('/api/templates/dalala-cover-001/rules',null,clientA.cookie)).status,403)});
test('approved default muse preview and shortcut use the selected identity image',async()=>{
 assert.equal((await req('/api/model-assets/default',{},clientA.cookie)).status,403);
 const ownerState=await req('/api/state',null,admin.cookie),clientState=await req('/api/state',null,clientA.cookie);
 assert.equal(ownerState.d.defaultModel.modelId,'dalala-cover-muse-007');
 assert.equal(clientState.d.defaultModel,null);
 const preview=await fetch(base+'/api/model-assets/default/preview',{headers:{Cookie:admin.cookie}});
 assert.equal(preview.status,200);
 assert.equal(preview.headers.get('content-type'),'image/png');
 assert.deepEqual(Buffer.from(await preview.arrayBuffer()),await fs.readFile(path.join(root,'model-assets/dalala-cover-muse-007/reference/white-top-wall-master.png')));
 const first=await req('/api/model-assets/default',{},admin.cookie),second=await req('/api/model-assets/default',{},admin.cookie);
 assert.equal(first.status,200);
 assert.equal(first.d.modelId,'dalala-cover-muse-007');
 assert.equal(second.d.id,first.d.id);
 assert.equal((await fetch(base+first.d.url,{headers:{Cookie:admin.cookie}})).status,200);
});
test('unpublished templates stay out of customer catalog',async()=>{const a=await req('/api/state',null,admin.cookie),b=await req('/api/state',null,clientA.cookie);assert.equal(a.d.templates.length,initialReferenceCount);assert.ok(b.d.templates.every(t=>t.published))});
test('upload ownership enforced for reads and jobs',async()=>{const b64='iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a3ioAAAAASUVORK5CYII=';upload=await req('/api/upload',{name:'test.png',type:'image/png',data:b64},clientA.cookie);assert.equal(upload.status,200);const forbidden=await fetch(base+upload.d.url,{headers:{Cookie:clientB.cookie}});assert.equal(forbidden.status,400);const j=await req('/api/jobs',{templateId:'dalala-cover-001',brief:'test',test:true,uploads:[{id:upload.d.id}]},admin.cookie);assert.equal(j.status,400)});
test('client cannot run backend jobs; untested templates cannot publish',async()=>{assert.equal((await req('/api/jobs',{kind:'study',templateId:'dalala-cover-001'},clientA.cookie)).status,400);assert.equal((await req('/api/templates/dalala-cover-001/finalize',{sampleJobId:'sample'},clientA.cookie)).status,403);assert.equal((await req('/api/templates/dalala-cover-001/finalize',{},admin.cookie)).status,400);assert.equal((await req('/api/templates/dalala-cover-001/publish',{published:true},admin.cookie)).status,400)});
test('latest completed decomposition can be confirmed and persists',async()=>{const id='study-fixture',dir=path.join(tmp,'jobs',id),createdAt=new Date().toISOString();await fs.mkdir(dir,{recursive:true});await fs.writeFile(path.join(dir,'analysis.md'),'# 拆解结果\n\n- 主体与标题关系已确认');await fs.writeFile(path.join(dir,'job.json'),JSON.stringify({id,userId:admin.d.user.id,templateId:'dalala-cover-001',kind:'study',status:'completed',createdAt,finishedAt:createdAt}));await fs.writeFile(path.join(tmp,'templates.json'),JSON.stringify({'dalala-cover-001':{latestStudyJobId:id,studiedAt:createdAt}}));assert.equal((await req('/api/templates/dalala-cover-001/confirm-analysis',{jobId:id},clientA.cookie)).status,403);assert.equal((await req('/api/templates/dalala-cover-001/confirm-analysis',{jobId:id},admin.cookie)).status,200);const state=await req('/api/state',null,admin.cookie),template=state.d.templates.find(t=>t.id==='dalala-cover-001');assert.equal(template.analysisConfirmedJobId,id);assert.ok(template.analysisConfirmedAt);assert.match((await req('/api/jobs/'+id+'/analysis',null,admin.cookie)).d.text,/拆解结果/)});
test('bad images, path traversal, foreign origins rejected',async()=>{assert.equal((await req('/api/upload',{name:'fake.png',type:'image/png',data:Buffer.from('no').toString('base64')},admin.cookie)).status,400);const r=await fetch(base+'/api/state',{headers:{Origin:'http://evil.example',Cookie:admin.cookie}});assert.equal(r.status,403);assert.equal((await req('/api/references',{uploadId:'../../secret'},admin.cookie)).status,400)});
test('customer cannot read another customer job',async()=>{const id='test-owned-job';await fs.mkdir(path.join(tmp,'jobs',id),{recursive:true});await fs.writeFile(path.join(tmp,'jobs',id,'job.json'),JSON.stringify({id,userId:clientA.d.user.id,status:'failed',createdAt:new Date().toISOString()}));assert.equal((await req('/api/jobs/'+id,null,clientB.cookie)).status,400);assert.equal((await req('/api/jobs/'+id,null,clientA.cookie)).status,200)});
test('missing static file cannot crash server',async()=>{const r=await fetch(base+'/missing-file.ico');assert.equal(r.status,400);assert.equal((await req('/api/auth')).status,200)});
test('front catalog excludes raw references even for administrator',async()=>{const r=await req('/api/state',null,admin.cookie);assert.equal(r.d.catalog.length,0);assert.equal(r.d.templates.length,initialReferenceCount);assert.equal((await fetch(base+'/assets/'+encodeURIComponent('参考封面图')+'/dalala-cover-ref-001.jpg',{headers:{Cookie:clientA.cookie}})).status,403)});
test('publishing requires a selected own-template sample and exposes only the copied sample',async()=>{const id='sample-fixture';const dir=path.join(tmp,'jobs',id);await fs.mkdir(dir,{recursive:true});await fs.writeFile(path.join(dir,'cover.png'),Buffer.from('test-only-sample-image'));await fs.writeFile(path.join(dir,'job.json'),JSON.stringify({id,userId:admin.d.user.id,templateId:'dalala-cover-001',kind:'render',status:'completed',createdAt:new Date().toISOString()}));assert.equal((await req('/api/templates/dalala-cover-001/publish',{published:true},admin.cookie)).status,400);assert.equal((await req('/api/templates/dalala-cover-001/publish',{published:true,sampleJobId:id},admin.cookie)).status,200);const r=await req('/api/state',null,clientA.cookie);assert.equal(r.d.catalog.length,1);assert.equal(r.d.catalog[0].reference,'/api/showcases/dalala-cover-001');assert.equal(r.d.templates[0].reference,r.d.catalog[0].reference);const img=await fetch(base+r.d.catalog[0].reference,{headers:{Cookie:clientA.cookie}});assert.equal(await img.text(),'test-only-sample-image');await req('/api/templates/dalala-cover-001/publish',{published:false},admin.cookie);assert.equal((await req('/api/state',null,admin.cookie)).d.catalog.length,0)});
test('login session survives a local service restart',async()=>{assert.equal((await req('/api/state',null,admin.cookie)).status,200);await new Promise(resolve=>{proc.once('exit',resolve);proc.kill()});await startServer();const restored=await req('/api/state',null,admin.cookie);assert.equal(restored.status,200);assert.equal(restored.d.user.id,admin.d.user.id)});
test('batch decomposition queues once and supports promote, pause, resume, cancel',async()=>{
 const templateIds=['dalala-cover-002','dalala-cover-003','dalala-cover-004','dalala-cover-005'];
 const submitted=await req('/api/jobs/batch-study',{templateIds},admin.cookie);assert.equal(submitted.status,201);assert.equal(submitted.d.jobs.length,4);
 const ids=submitted.d.jobs.map(j=>j.id);const duplicate=await req('/api/jobs/batch-study',{templateIds},admin.cookie);assert.equal(duplicate.d.jobs.length,0);assert.equal(duplicate.d.skipped,4);
 let jobs;for(let attempt=0;attempt<80;attempt++){jobs=(await req('/api/state',null,admin.cookie)).d.jobs.filter(j=>ids.includes(j.id));if(jobs.filter(j=>j.status==='running').length===3)break;await new Promise(resolve=>setTimeout(resolve,25))}
 assert.equal(jobs.filter(j=>j.status==='running').length,3,'three independent references should run simultaneously');
 assert.equal(jobs.filter(j=>j.status==='queued').length,1,'the fourth reference should wait for an available quality-controlled slot');
 const queued=jobs.find(j=>j.status==='queued'),running=jobs.find(j=>j.status==='running');
 assert.equal((await req('/api/jobs/'+queued.id+'/promote',{},admin.cookie)).status,200);
 assert.equal((await req('/api/jobs/'+running.id+'/pause',{},admin.cookie)).d.status,'paused');
 for(let attempt=0;attempt<80;attempt++){const current=await req('/api/jobs/'+queued.id,null,admin.cookie);if(current.d.status==='running')break;await new Promise(resolve=>setTimeout(resolve,25))}
 assert.equal((await req('/api/jobs/'+queued.id,null,admin.cookie)).d.status,'running');
 assert.equal((await req('/api/jobs/'+running.id+'/resume',{},admin.cookie)).status,200);
 for(const id of ids)await req('/api/jobs/'+id+'/cancel',{},admin.cookie);
 assert.equal((await req('/api/jobs/batch-study',{templateIds:['dalala-cover-004']},clientA.cookie)).status,400);
});

test('workbench launches Codex with GPT-6 Sol and medium reasoning',async()=>{
 const submitted=await req('/api/jobs/batch-study',{templateIds:['dalala-cover-002']},admin.cookie);
 assert.equal(submitted.d.jobs.length,1);
 let args;
 for(let i=0;i<80;i++){args=await fs.readFile(path.join(tmp,'codex-args.txt'),'utf8').catch(()=>null);if(args)break;await new Promise(resolve=>setTimeout(resolve,25))}
 assert.ok(args,'the fake executor should capture the workbench Codex arguments');
 const parts=args.trim().split('\n');
 assert.deepEqual(parts.slice(parts.indexOf('--model'),parts.indexOf('--model')+2),['--model','gpt-6-sol']);
 assert.deepEqual(parts.slice(parts.indexOf('--config'),parts.indexOf('--config')+2),['--config','model_reasoning_effort=medium']);
 await req('/api/jobs/'+submitted.d.jobs[0].id+'/cancel',{},admin.cookie);
});

test('retry preserves inputs and prevents duplicate queue entries',async()=>{
 const id='retry-fixture',dir=path.join(tmp,'jobs',id),job={id,userId:admin.d.user.id,kind:'render',templateId:'dalala-cover-012',test:true,brief:'原来的测试内容',uploads:[{id:'kept-material'}],status:'failed',error:'旧失败原因',createdAt:new Date().toISOString(),finishedAt:new Date().toISOString()};
 await fs.mkdir(dir,{recursive:true});await fs.writeFile(path.join(dir,'job.json'),JSON.stringify(job));await fs.writeFile(path.join(dir,'result.json'),JSON.stringify({ok:true,output:'old.png'}));
 assert.equal((await req('/api/jobs/'+id+'/retry',{},clientA.cookie)).status,400);
 const retried=await req('/api/jobs/'+id+'/retry',{},admin.cookie);assert.equal(retried.status,200);assert.equal(retried.d.id,id);assert.equal(retried.d.brief,job.brief);assert.deepEqual(retried.d.uploads,job.uploads);assert.equal(retried.d.retryCount,1);assert.equal(retried.d.error,undefined);
 await assert.rejects(fs.access(path.join(dir,'result.json')));assert.equal((await req('/api/jobs/'+id+'/retry',{},admin.cookie)).status,400);
 await req('/api/jobs/'+id+'/pause',{},admin.cookie);assert.equal((await req('/api/jobs/'+id+'/retry',{},admin.cookie)).status,200);await req('/api/jobs/'+id+'/cancel',{},admin.cookie);
});

test('published covers can return to the lab or be removed with contiguous catalog numbers',async()=>{
 const registryPath=path.join(tmp,'registry.json'),metaPath=path.join(tmp,'templates.json');
 const registry=JSON.parse(await fs.readFile(registryPath,'utf8')),meta=JSON.parse(await fs.readFile(metaPath,'utf8'));
 for(const id of ['dalala-cover-001','dalala-cover-002','dalala-cover-003']){
  registry.skills.find(t=>t.id===id).status='active';
  meta[id]={...meta[id],showcaseFile:`showcases/${id}.png`,analysisConfirmedAt:'2026-09-01T00:00:00.000Z'};
  await fs.mkdir(path.join(tmp,'showcases'),{recursive:true});await fs.writeFile(path.join(tmp,meta[id].showcaseFile),'sample');
 }
 await fs.writeFile(registryPath,JSON.stringify(registry));await fs.writeFile(metaPath,JSON.stringify(meta));
 const before=await req('/api/state',null,clientA.cookie);
 assert.deepEqual(before.d.catalog.slice(0,3).map(t=>[t.id,t.sequence]),[['dalala-cover-001',1],['dalala-cover-002',2],['dalala-cover-003',3]]);
 assert.equal((await req('/api/templates/dalala-cover-002/delete',{},clientA.cookie)).status,403);
 assert.equal((await req('/api/templates/dalala-cover-002/delete',{},admin.cookie)).status,200);
 const afterDelete=await req('/api/state',null,clientA.cookie);
 assert.deepEqual(afterDelete.d.catalog.slice(0,2).map(t=>[t.id,t.sequence]),[['dalala-cover-001',1],['dalala-cover-003',2]]);
 assert.equal((await req('/api/state',null,admin.cookie)).d.templates.some(t=>t.id==='dalala-cover-002'),false);
 assert.equal((await req('/api/templates/dalala-cover-002/delete',{},admin.cookie)).status,400);
 assert.equal((await req('/api/jobs',{templateId:'dalala-cover-002',kind:'render',test:true,brief:'deleted'},admin.cookie)).status,400);
 assert.equal((await req('/api/templates/dalala-cover-003/return',{},admin.cookie)).status,200);
 const returned=(await req('/api/state',null,admin.cookie)).d.templates.find(t=>t.id==='dalala-cover-003');
 assert.equal(returned.status,'testing');assert.equal(returned.published,false);assert.ok(returned.returnedAt);assert.equal(returned.showcase,null);
 assert.equal((await req('/api/state',null,clientA.cookie)).d.catalog.some(t=>t.id==='dalala-cover-003'),false);
 const premature=await req('/api/templates/dalala-cover-003/finalize',{},admin.cookie);
 assert.equal(premature.status,400);assert.match(premature.d.error,/返厂后请先完成一次新的复刻测试/);
});

test('a pending reference can be removed only when no decomposition is active',async()=>{
 const registryPath=path.join(tmp,'registry.json'),metaPath=path.join(tmp,'templates.json');
 const registry=JSON.parse(await fs.readFile(registryPath,'utf8')),meta=JSON.parse(await fs.readFile(metaPath,'utf8'));
 const id='dalala-cover-038';registry.skills.find(t=>t.id===id).status='intake';delete meta[id]?.showcaseFile;
 await fs.writeFile(registryPath,JSON.stringify(registry));await fs.writeFile(metaPath,JSON.stringify(meta));
 const jobId='pending-delete-fixture',dir=path.join(tmp,'jobs',jobId);await fs.mkdir(dir,{recursive:true});await fs.writeFile(path.join(dir,'job.json'),JSON.stringify({id:jobId,userId:admin.d.user.id,templateId:id,kind:'study',status:'queued',createdAt:new Date().toISOString()}));
 const busy=await req('/api/templates/'+id+'/delete',{},admin.cookie);assert.equal(busy.status,400);assert.match(busy.d.error,/先在任务记录中取消/);
 const job=JSON.parse(await fs.readFile(path.join(dir,'job.json'),'utf8'));job.status='cancelled';await fs.writeFile(path.join(dir,'job.json'),JSON.stringify(job));
 assert.equal((await req('/api/templates/'+id+'/delete',{},clientA.cookie)).status,403);
 assert.equal((await req('/api/templates/'+id+'/delete',{},admin.cookie)).status,200);
 assert.equal((await req('/api/state',null,admin.cookie)).d.templates.some(t=>t.id===id),false);
});
