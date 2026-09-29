#import <Cocoa/Cocoa.h>
#import <UniformTypeIdentifiers/UniformTypeIdentifiers.h>
#import <WebKit/WebKit.h>

@interface DalalaCoverAppDelegate : NSObject <NSApplicationDelegate, WKNavigationDelegate, WKUIDelegate, WKDownloadDelegate>
@property(nonatomic, strong) NSWindow *window;
@property(nonatomic, strong) WKWebView *webView;
@property(nonatomic, strong) NSTask *serverProcess;
@end

@implementation DalalaCoverAppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)notification {
    [NSApp setActivationPolicy:NSApplicationActivationPolicyRegular];
    [self configureMenus];

    if (![self startRequiredService]) {
        [self showFailure:@"后台服务启动失败，当前账号、任务和素材不会丢失。请稍后重新打开。"];
        return;
    }

    [self configureWindow];
    [NSApp activateIgnoringOtherApps:YES];
    [self.webView loadRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:@"http://127.0.0.1:4318/"]
                                               cachePolicy:NSURLRequestReloadRevalidatingCacheData
                                           timeoutInterval:30]];
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
    return YES;
}

- (void)configureMenus {
    NSMenu *mainMenu = [[NSMenu alloc] init];
    NSMenuItem *appMenuItem = [[NSMenuItem alloc] init];
    [mainMenu addItem:appMenuItem];
    NSMenu *appMenu = [[NSMenu alloc] initWithTitle:@"Dalala 封面工作台"];
    [appMenu addItemWithTitle:@"关于 Dalala 封面工作台" action:@selector(orderFrontStandardAboutPanel:) keyEquivalent:@""];
    [appMenu addItem:[NSMenuItem separatorItem]];
    [appMenu addItemWithTitle:@"退出 Dalala 封面工作台" action:@selector(terminate:) keyEquivalent:@"q"];
    appMenuItem.submenu = appMenu;

    NSMenuItem *editMenuItem = [[NSMenuItem alloc] init];
    [mainMenu addItem:editMenuItem];
    NSMenu *editMenu = [[NSMenu alloc] initWithTitle:@"编辑"];
    [editMenu addItemWithTitle:@"撤销" action:@selector(undo:) keyEquivalent:@"z"];
    [editMenu addItemWithTitle:@"重做" action:@selector(redo:) keyEquivalent:@"Z"];
    [editMenu addItem:[NSMenuItem separatorItem]];
    [editMenu addItemWithTitle:@"剪切" action:@selector(cut:) keyEquivalent:@"x"];
    [editMenu addItemWithTitle:@"复制" action:@selector(copy:) keyEquivalent:@"c"];
    [editMenu addItemWithTitle:@"粘贴" action:@selector(paste:) keyEquivalent:@"v"];
    [editMenu addItemWithTitle:@"全选" action:@selector(selectAll:) keyEquivalent:@"a"];
    editMenuItem.submenu = editMenu;
    NSApp.mainMenu = mainMenu;
}

- (BOOL)startRequiredService {
    NSString *script = [NSBundle.mainBundle pathForResource:@"ensure-server" ofType:@"sh"];
    if (!script) return NO;
    self.serverProcess = [[NSTask alloc] init];
    self.serverProcess.executableURL = [NSURL fileURLWithPath:@"/bin/zsh"];
    self.serverProcess.arguments = @[script];
    self.serverProcess.standardOutput = [NSFileHandle fileHandleWithNullDevice];
    self.serverProcess.standardError = [NSFileHandle fileHandleWithNullDevice];
    NSError *error = nil;
    if (![self.serverProcess launchAndReturnError:&error]) return NO;
    for (NSInteger attempt = 0; attempt < 80; attempt++) {
        NSTask *probe = [[NSTask alloc] init];
        probe.executableURL = [NSURL fileURLWithPath:@"/usr/bin/curl"];
        probe.arguments = @[@"-fsS", @"--max-time", @"2", @"http://127.0.0.1:4318/api/auth"];
        probe.standardOutput = [NSFileHandle fileHandleWithNullDevice];
        probe.standardError = [NSFileHandle fileHandleWithNullDevice];
        if ([probe launchAndReturnError:nil]) {
            [probe waitUntilExit];
            if (probe.terminationStatus == 0) return YES;
        }
        [NSThread sleepForTimeInterval:0.25];
    }
    if (self.serverProcess.running) [self.serverProcess terminate];
    return NO;
}

- (void)applicationWillTerminate:(NSNotification *)notification {
    if (self.serverProcess.running) [self.serverProcess terminate];
}

- (void)configureWindow {
    WKWebViewConfiguration *configuration = [[WKWebViewConfiguration alloc] init];
    configuration.websiteDataStore = WKWebsiteDataStore.defaultDataStore;
    self.webView = [[WKWebView alloc] initWithFrame:NSZeroRect configuration:configuration];
    self.webView.navigationDelegate = self;
    self.webView.UIDelegate = self;

    self.window = [[NSWindow alloc]
        initWithContentRect:NSMakeRect(0, 0, 1360, 900)
        styleMask:NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable
        backing:NSBackingStoreBuffered
        defer:NO];
    self.window.title = @"Dalala 封面工作台";
    self.window.minSize = NSMakeSize(960, 680);
    self.window.contentView = self.webView;
    [self.window center];
    [self.window makeKeyAndOrderFront:nil];
}

- (void)showFailure:(NSString *)message {
    NSAlert *alert = [[NSAlert alloc] init];
    alert.alertStyle = NSAlertStyleCritical;
    alert.messageText = @"Dalala 封面工作台未能启动";
    alert.informativeText = message;
    [alert runModal];
    [NSApp terminate:nil];
}

- (void)webView:(WKWebView *)webView
runOpenPanelWithParameters:(WKOpenPanelParameters *)parameters
initiatedByFrame:(WKFrameInfo *)frame
completionHandler:(void (^)(NSArray<NSURL *> * _Nullable URLs))completionHandler {
    NSOpenPanel *panel = [NSOpenPanel openPanel];
    panel.canChooseFiles = YES;
    panel.canChooseDirectories = NO;
    panel.allowsMultipleSelection = parameters.allowsMultipleSelection;
    panel.allowedContentTypes = @[UTTypeImage];
    [panel beginSheetModalForWindow:self.window completionHandler:^(NSModalResponse response) {
        completionHandler(response == NSModalResponseOK ? panel.URLs : nil);
    }];
}

- (void)webView:(WKWebView *)webView
decidePolicyForNavigationAction:(WKNavigationAction *)navigationAction
preferences:(WKWebpagePreferences *)preferences
decisionHandler:(void (^)(WKNavigationActionPolicy, WKWebpagePreferences *))decisionHandler {
    if (navigationAction.shouldPerformDownload) {
        decisionHandler(WKNavigationActionPolicyDownload, preferences);
        return;
    }
    NSURL *url = navigationAction.request.URL;
    NSString *host = url.host;
    if (host && ![host isEqualToString:@"127.0.0.1"] && ![host isEqualToString:@"localhost"]) {
        [NSWorkspace.sharedWorkspace openURL:url];
        decisionHandler(WKNavigationActionPolicyCancel, preferences);
        return;
    }
    decisionHandler(WKNavigationActionPolicyAllow, preferences);
}

- (void)webView:(WKWebView *)webView navigationAction:(WKNavigationAction *)navigationAction didBecomeDownload:(WKDownload *)download {
    download.delegate = self;
}

- (void)webView:(WKWebView *)webView navigationResponse:(WKNavigationResponse *)navigationResponse didBecomeDownload:(WKDownload *)download {
    download.delegate = self;
}

- (void)download:(WKDownload *)download
decideDestinationUsingResponse:(NSURLResponse *)response
suggestedFilename:(NSString *)suggestedFilename
completionHandler:(void (^)(NSURL * _Nullable destination))completionHandler {
    NSSavePanel *panel = [NSSavePanel savePanel];
    panel.nameFieldStringValue = suggestedFilename;
    panel.allowedContentTypes = @[UTTypePNG];
    panel.canCreateDirectories = YES;
    [panel beginSheetModalForWindow:self.window completionHandler:^(NSModalResponse result) {
        completionHandler(result == NSModalResponseOK ? panel.URL : nil);
    }];
}

- (void)downloadDidFinish:(WKDownload *)download {
    [[NSSound soundNamed:@"Glass"] play];
}

- (void)download:(WKDownload *)download didFailWithError:(NSError *)error resumeData:(NSData *)resumeData {
    NSAlert *alert = [[NSAlert alloc] init];
    alert.alertStyle = NSAlertStyleWarning;
    alert.messageText = @"图片保存失败";
    alert.informativeText = @"请重新点击“点击保存”。";
    [alert beginSheetModalForWindow:self.window completionHandler:nil];
}

- (nullable WKWebView *)webView:(WKWebView *)webView
createWebViewWithConfiguration:(WKWebViewConfiguration *)configuration
forNavigationAction:(WKNavigationAction *)navigationAction
windowFeatures:(WKWindowFeatures *)windowFeatures {
    if (navigationAction.request.URL) {
        [NSWorkspace.sharedWorkspace openURL:navigationAction.request.URL];
    }
    return nil;
}

@end

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        NSApplication *application = NSApplication.sharedApplication;
        DalalaCoverAppDelegate *delegate = [[DalalaCoverAppDelegate alloc] init];
        application.delegate = delegate;
        [application run];
    }
    return 0;
}
