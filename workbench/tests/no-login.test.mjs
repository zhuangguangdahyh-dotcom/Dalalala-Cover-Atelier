import {test,after,before} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const port=14321,base=`http://127.0.0.1:${port}`,root=path.resolve('..');
let proc,tmp;
before(async()=>{
 tmp=await fs.mkdtemp(path.join(os.tmpdir(),'dalala-no-login-test-'));
 await fs.copyFile(path.join(root,'cover-skills/registry.json'),path.join(tmp,'registry.json'));
 await fs.writeFile(path.join(tmp,'users.json'),JSON.stringify([{id:'existing-owner',email:'owner@test.local',name:'Dalala',role:'admin'}]));
 const jobDir=path.join(tmp,'jobs','saved-job');await fs.mkdir(jobDir,{recursive:true});
 await fs.writeFile(path.join(jobDir,'job.json'),JSON.stringify({id:'saved-job',userId:'existing-owner',kind:'render',status:'failed',createdAt:new Date().toISOString()}));
 proc=spawn(process.execPath,['server.mjs'],{env:{...process.env,PORT:String(port),DALALA_DATA_DIR:tmp,DALALA_REGISTRY:path.join(tmp,'registry.json')},stdio:['ignore','pipe','pipe']});
 await new Promise((resolve,reject)=>{proc.stdout.once('data',resolve);proc.once('error',reject);proc.once('exit',()=>reject(Error('Server stopped')))});
});
after(async()=>{proc?.kill();if(tmp)await fs.rm(tmp,{recursive:true,force:true})});

test('local workbench opens without login and keeps existing owner history',async()=>{
 const state=await fetch(base+'/api/state');assert.equal(state.status,200);
 const data=await state.json();assert.equal(data.user.id,'existing-owner');assert.equal(data.user.role,'admin');
 assert.ok(data.jobs.some(j=>j.id==='saved-job'));
 const job=await fetch(base+'/api/jobs/saved-job');assert.equal(job.status,200);
 const auth=await (await fetch(base+'/api/auth')).json();assert.equal(auth.needsSetup,false);assert.equal(auth.localNoLogin,true);
 const login=await fetch(base+'/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:'owner@test.local',password:'old-password'})});assert.equal(login.status,400);
});
