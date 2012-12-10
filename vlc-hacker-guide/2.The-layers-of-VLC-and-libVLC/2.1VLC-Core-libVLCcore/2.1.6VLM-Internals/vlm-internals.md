#vlm内部

##1.介绍

VideoLAN控制的是一个小型的媒体管理器，控制多个数据流的VLC。它允许多个数据流和视频点播（VoD）。 VLM可以通过Telnet和HTTP接口文档控制VLC：Streaming_HowTo/ VLM。
本文档将描述，VLM包括数据的结构和功能，以及libvlc绑定控制VLM的内部。

##2.vlm_t

在VLC或libvlc中VLM只有一个可以运行。例如VLM为代表的结构vlm_t在src/input/vlm_internal.h的定义。vlm_t包含了一系列的媒体，附表和VOD服务器，以及一个视频播放交互技术的数据结构，以及一个唯一的ID。本质上，vlm_t的数据结构是全局容器，以及全部的VLM的相关数据.

##3 媒体和实例

一个媒体组成的列表输入，输出和一些选项
有两种类型的媒体：

*  Vod  常用的视频点播，只有当用户请求的时候才会运行

*  Broadcast广播媒体与电视节目和通道非常接近，它可以由管理员启动，停止或暂停，也可以重复几次

由结构定义在src /input/ vlm_internal.h的的vlm_media_sys_t的一个媒体表示。每个vlm_media_sys_t包含的配置结构，媒体的实例的列表，以及代表VOD服务器的结构，这是只有在初始化的媒体类型（VOD配置结构的类型vlm_media_t，包含的媒体名称，以及它的类型和主机的其他细节。它的定义在src /input/ vlm_internal.h。

一个媒体实例代表在src /input/ vlm_internal.h的定义的结vlm_media_instance_sys_t，中。这个结构包含一个播放列表中的索引，以及当前的输入线和输出流实例。多张的媒体实例可以存在于每个媒体。

每个VOD服务器表示的结构vod_t。该结构包含一个指向将被加载的模块，以帮助VOD服务器，以及指针，指向一个RTSP服务器。它还包含几个函数指针，以帮助创建和删除VOD媒体类型。

vod_media_t。如果该媒体VOD类型,则实际引用的每个vod_media_t。
vlm_media_sys_t， vod_t定义在include / vlc_vod.h和中定义模块/ MISC / rtsp.c的vod_media_t

Vlm 的主要布局：

vlm_t

vlm_media_sys_t

vlm_media_t

vlm_media_instance_sys_t

vod_media_t

vod_t

##4 附表

##5 初始化VLM和添加媒体

VLM是libvlc的一部分，我将描述VLM就libvlc的初始化。如果我们要使用VLM，我们至少有一个媒体。因此，我们可以使用libvlc的功能libvlc_vlm_add_broadcast（）或libvlc_vlm_add_vod（）实例化和初始化VLM。检查这些中的每一个功能，看看是否存在一个VLM实例。如果没有，该功能创建一个vlm_t的实例，并创建和增加广播或点播媒体的vlm_t实例。如果媒体类型是视频点播，然后一个单独的vod_media_t被创建和链接到的类型vlm_media_sys_t媒体和视频点播服务类型vod_t被创建并关联的vlm_t实例。
还请注意，VLM实例连接到一个单独的libvlc实例，因此只允许一个VLM每libvlc实例的实例。这两个libvlc_vlm_add_broadcast（）和libvlc_vlm_add_vod（）环绕的VLM（）宏包装周围__ vlm_New的（），它实际做的实例化，初始化，并具有约束力的VLM实例的libvlc实例。

##6 控制

一旦被初始化VLM，需要有某种方式来控制它，如添加媒体，媒体实例启动和停止等..

vlm_Control（）函数是用于此目的。这使得所有VLM发出的命令通过一个共同的接口，它需要照顾的锁定问题。通过与适当的命令代码，如VLM_ADD_MEDIA，和变量参数列表的执行

vlm_Control（），任何的VLM命令可以被执行，而无需了解低级别的细节。这使得容易包装的的VLM代码使用的许多接口。 vlm_Control（）可以找到在src/输入/ vlm.c的。 VLM命令代码的列表中可以找到在该文件中的枚举类型vlm_query_e包括/ vlc_vlm.h。
 
##7创建线程

VLM内VLC是一个复杂的子系统。VLM被初始化，媒体被创建等..，线程被创建来处理这些任务。本节将介绍使用VLM的线程模型。   

当新的实例VLM的的__ vlm_New（）函数创建，管理线程创建具有启动功能管理在src/输入/ vlm.c的的。这需要考虑调度，以及输入对象的破坏。      

当一个新的视频点播媒体添加到VLM，输入创建的线程的run（）作为其启动功能。此线程处理所有的流媒体，媒体。  

它需要播放添加的广播媒体，。当libvlc的功能libvlc_vlm_play_media（）被调用时，广播媒体的一个实例被创建和启动功能的输入线程的run（）。线程处理所有的流媒体广播实例，通过调用相应的解复用，解码器，和SOUT模块