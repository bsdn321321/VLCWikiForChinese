nterface
=========================================
#接口
*  1.1一个典型的vlc运行过程
 本节将会描述当你启动VLC程序时，会发生什。在ELF动态加载之后，主要线程将转变为界面线程
   
    1.CPU检测：CPU的运行位置，功能  

    2.信息接口的初始化  

    3.数据包选项解析

    4.列表的创作

    5.模块初始化

    6.接口开放

    7.信号处理程序的安装：SIGHUP,SIGINT和SIGQUIT的退出（请注意SDL库也捕获SIGSEGV)；

    8.音频输出线程的扩展

    9.视频输出线程的扩展

    10.主要循环：事件管理

以下各点描述这些步骤。

*  1.2消息接口

众所周知，printf()函数不一定是线程安全的。因此，在Printf（）中，一个线程调用，另一个调用它的线程中断，将会使程序处于不确定状态。因此，一个API必须在没有崩溃的情况下设置打印信息。

这个API是用两种方式实现的。如果INTF_MSG_QUEUE被定义在config.h中，每一个类似printf呼叫到一个列表队列的信息。这个列表将会由接口线程在每一次循环的时候打印和刷新。如果INTF_MSG_QUEUE没有定义，调用线程将获得打印锁定和直接打印。

打印消息的函数：

msg_Info（p_this，...）：打印一条消息到stdout，plain和stupid(例如“it works!")

msg_Err（p_this，...）：一个错误信息打印到stderr

msg_Warn（p_this，...）：打印一条消息到stderr，如果警告级别（由-V，-vv和VVV）是足够低。请注意，如果是较低的电平，该消息不那么重要的。

msg_Dbg（p_this，...）：这个函数是检查可选点的消息，如“我们现在进入功能dvd_foo_thingy的”。

没有在非跟踪模式。如果在VLC编译时加上enable跟踪，，该消息要么被写入文件vlc-trace.log，或者输出到stderr.

msg_Flush(p_this) 如果它正在使用，刷新消息队列

*  1.3命令行选项

VLC使用GNU getopt来分析命令行选项。 getopt的结构定义在src/extras/ getopt.c和在src/extras/ cmdline.c的命令行解析完成的。

通过环境数组中中的大多数配置指令进行交换，使用main_Put*的变量和main_Get*变量。其结果是，/VLC - 高度240严格等于：vlc_height= 240/ vlc的。这样的配置变量，包括插件是随处可见的。

 1.3.1警告

请注意线程安全问题，当第二个线程产生后，不应该使用main_Put*变量。


1.4播放列表管理

启动时在命令行中指定的文件创建播放列表。一个合适的接口插件也可以添加或删除的文件。使用的函数在 SRC/playlist/ control.c中。

后者则部分描述如何写一个插件。其他线程可以请求一个插件描述用module_Need（module_bank_t p_bank，INT i_capabilities，void *的P_DATA）。 P_DATA的pf_probe（）函数是一个可选的参数（保留，以备将来使用）。返回module_t结构包含指针的功能的插件。查看包含/ modules.h的更多信息

1.5接口的主回路

界面线程会先寻找一个合适的接口插件。然后进入主界面循环，用插件的pf_run函数。这个函数将每100毫秒调用然后做最合适的选择，（通常通过一个GUI定时器回调）。

相互作用控制清理卸载不需要的模块，模块的本地管理播放，并刷新消息（如果在使用消息队列）。

1.6如何写一个界面插件

 1.6.1API模块

看看模块的/ misc/control/ misc/access，或modules/ GUI目录中的文件。然而，图形用户界面不是很容易理解的，因为他们是相当大的。我认为首先先深入一个非图形界面模块。例如module/control/ hotkeys.c。

一个接口模块由三个主要函数和一个模块描述组成：


 用它的优先级模块描述宏声明的功能模块。因为它会出现在GUI模块中，一下配置随着模块，快捷方式和子模块的不同改变。

    打开（vlc_object_t p_object）：这就是所谓的VLC初始化模块。

    运行（vlc_object_t p_object）：确实工作的接口模块（等待用户输入和显示信息）。应定期检查，p_intf - > b_die不是VLC_TRUE。

    关闭（vcl_object_t p_object）函数被调用的VLC取消初始化模块（基本上，这包括在销毁任何已分配由开放）

上面的函数需要一个vlc_object_t*作为参数，但可能需要根据您的需要转换到一个intf_thread_t*。这种结构通常需要作为一个参数导出VLC功能，如msg_Err msg_Warn（），...

定义intf_sys_t包含任何你所需要的（不使用静态变量，多线程应用程序:-)。

   在GUImodule之一 如果需要额外的功能（如打开“按钮，播放列表，菜单等）。一个简单的GUImodule咨询可能是在模块/ GUI/ ncurses/ ncurses.c。这是一个很简单的完整的接口模块的播放列表互动，进度条，和其他事项。

