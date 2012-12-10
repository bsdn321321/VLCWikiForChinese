#输入
------------------------------------------------------------------------
##1复杂的多层输入

输入模块背后的想法是在不知道里边有什么东西的情况下还原数据包。它只需要获取一个数据包，读取其ID，并将它在正确的时间传递到解码器中的数据包报头（在MPEG中的SCR和PCR字段）。所有的基本的浏览操作是在不查看的基本流的内容的情况下完成的。

因此，它仍然是非常通用的。这也意味着你不能做的东西，像“播放3帧”或“前进10帧”或“以能够到达的最快的速度播放所有帧”。它甚至不知道什么是“帧”。它里边没有特权的基本流，如视频（，原因很简单，根据MPEG，一个流可能包含多个视频ES）。
对于文件的处理

###1.1文件中发生的。

每一个读取的文件都会对应生成一个输入线程。事实上，输入结构和解码器需要重新初始化，因为可能会有不同的数据流。 input_CreateThread被界面线程所调用（播放列表模块）。

起初，VLC会通过调用功能模块 - > pf_activate，打开访问的流或access_demux模块，如果成功的话，该模块线程会被启动，同时vlc可以寻找一个demux module去复用一个access module的输出。

###1.2流管理

已经被调用的功能必须指定两个属性：

p_input - > stream.b_pace_control：是否可以读取数据流根据我们的需求（由流的频率和主机的系统时钟确定）。例如，一个文件或管道（包括TCP / IP连接）可以从我们的pace中读出，如果我们读取的速度不够快，管道的另一端将会因为write（）操作而阻塞。与此相反，UDP数据流（如的VideoLAN的服务器所使用的）是在服务器的pace，如果我们读取的速度不够快，在内核缓冲区已满时，数据包将丢失。所以对于服务器的时钟必须定期进行补偿。此属性控制时钟管理，控制是否可以快进和减慢镜头。

时钟管理中的subtilities：与一个UDP套接字以及一个遥远的服务器，漂移是不可忽略的，因为时钟发生细微改变，整个电影将会导致几秒的错时。在一定程度上，这意味着该演示文稿日期的输入线程与每个基本流的频率基本同步。因此输出的线程（如解码器线程）必须处理这个问题。

在设备与（如video4linux‘s​​/ dev /视频）读取的视频编码板进行连接时可能会发生同样的问题目前我们没有办法可以把它从简单的catfoo.mpg/VLC - 区分出来，但这并不意味着有任何时钟问题。所以将会询问（c）用户关于b_pace_control的价值的正确的事情，但没有人会明白它的意思（你是不是地球上最愚蠢的人，很明显，你多次读这一段会理解它： - ）。无论如何，漂移应该是可以忽略不计，因为CPU将共用相同的时钟，所以我们选择忽视它。

p_input->stream.b_seekable : 决定我们是否可以在文件descriptor中进行lseek()呼叫。基本上我们是否能跳到数据流的任何地方（从而显示滚动条）或者如果我们只能读取一个字节在这之后。这相比之前的项目流管理的影响较小，但它并不是多余的，因为例如cat foo.mpg VLC - 是=b_pace_control= 1但是b_seekable的= 0。相反，你可以没有b_seekable = 1 = 0 和b_pace_control。如果流是可查找，p_input> stream.p_selected_area> i_size必须被设置（在任意单元，例如字节，但它必须是相同p_input-> i_tell 这表明我们目前从流读取的字节）。
####1.2.1时间转换的偏移量

管理时钟的功能在src /input/ input_clock.c中。我们对一个文件的所有了解是它的起始偏移量和结束偏移量（p_input - > stream.p_selected_area - > i_size），目前以字节为单位，但它可能是plugin-dependant。那么，我们怎样才可以在界面中显示以秒为单位的时间？PS流有mux_rate的属性，它表明我们在一秒钟应该读多少字节。这是可以在任何时候变更的，但实际上，它是我们所知道的所有数据流的一个常量。因此，我们用它来确定时间偏移。

###1.3接口的结构出口

让我们集中于输入模块和接口之间的通信API。最重要的文件是/ vlc_input.h，它定义了input_thread_t结构，包括/ input_internal.h流描述符结构（在接入和多路分配器）stream__t，并包括/ vlc_esout.h的ES的描述。

首先，请注意，，input_thread_t structure feature two void *pointers,，p_method_data和p_plugin_data，您可以分别注明使用缓冲区管理数据和插件数据.

其次，流描述存储在包含几个基本流描述符的一个程序 描述的树中对于那些你不知道的所有的MPEG的概念，基本流，又名ES，是一个连续的流的视频（独家）音频数据，可以直接被解码器读取，无解封装。

这个树结构如下图所示，其中一个流拥有两个program。在大多数情况下只会有一个program（据我所知，只有TS流可以携带多个program，例如电影和足球比赛可以在同一时间 - 这对于卫星电视和有线电视广播已经足够了）。


####1.3.1警告

对于所有的修改和对p_input - >stream structure的访问，你必须持有p_input的 - > stream.stream_lock。

ES将会被一个ID描述（ID将寻找适当的解复用器），一个stream_id（真正的MPEG流ID），类型（定义在ISO / IEC 13818-1表2-29）和一个litteral的描述。它也包含上下文信息的多路分离器和解码器信息p_decoder_fifo，我们将在下一章节讨论。如果你想读的数据流不是一个MPEG系统层（用于比如AVI或RTP），一个特定的多路信号分离器将被写入。在这种情况下，如果您需要携带额外的信息，您可以使用void * p_demux_data在。在关机时，它会自动释放。

####1.3.2为什么使用ID而不使用普通的MPEG的stream_id？

当一个数据包（一个TS包，PS包，或任何）被读取时，相应的解复用器将在数据包中寻找一个ID，找到相关的基本流解复用，如果用户选择了它。在TS数据包的情况下，我们的唯一信息是在ES的PID，所以，我们保持的参考ID是PID。 PID在PS数据流是不存在的，所以我们必须生成一个。这当然是基于所有的PS数据包中发现的stream_id，由于专用流，它是不够的，（即AC3，SPU LPCM）都共用相同的stream_id（0xBD）。在这种情况下，流的第一个字节的PES的有效载荷是一个私人的ID，所以我们将stream_id与我们的ID相结合（如果你不明白一切，它就不是非常重要了 - 只记得我们用我们的大脑，然后再写入代码:-)。

流，程序和ES结构都充满插件的pf_init（）在src /输入/ input_programs.c的使用功能，但在任何时候都可以变更。DVD插件解析。从ifo files可以知道流中有哪个ES，TS插件读取流中的PAT和PMT结构，PS插件可以解析的PSM的结构（但很少出现），或由预解析的第一个兆字节的数据构建树“on the fly”，。
####1.3.3警告

在大多数情况下，我们需要预解析（即读取第一个MB的数据，并返回到开始）一个PS流，因为PSM（程序流图）结构几乎是不存在的。虽然，这是不合适的，但我们没有选择。一些可能会出现的问题。首先，不可查找的流不能预先解析，所以ES的树将被建在fly第二，如果一个新的基本流在第一个MB的数据后开始，在我们遇到的第一个数据包之前，它不会出现在菜单中，。我们不能预先解析整个流，因为它会占用几个小时（甚至没有对其进行解码）。

###1.4接口所使用的方法

这是目前的输入插件产生所需的解码器线程的职责。在选定的ES它必须调用input_SelectES，（input_thread_t p_input，es_descriptor_t“*”p_es“）。

流描述符包含的区域列表。区域在流中是逻辑不连续性的，例如在DVD的章节和标题。虽然我们可以使用它们在它们的的PSM（或PAT / PMT）版本变化时，但是在TS和PS流只有一个区域。我们的目标是，当你寻找到其他地方，输入插件加载新的流描述符树（否则所选择的ID可能是错误的）。
接口所使用的方法

此外，input_ext intf.c控制读取​​的流提供了一些功能：

input_SetStatus（input_thread_t p_input，诠释i_mode）：阅读变化的步伐。 i_mode可以之一INPUT_STATUS_END，INPUT_STATUS_PLAY，INPUT_STATUS_PAUSE，INPUT_STATUS_FASTER，INPUT_STATUS_SLOWER。

####1.4.1注意

在内部，阅读速度是由p_input的 - > stream.control.i_rate确定的。其默认值是DEFAULT_RATE。该值越低，则越快。速率变动由input_ClockManageRef所控制。暂停是通过简单地停止输入线程实现的（然后它会唤醒一个pthread信号）。在这种情况下，解码器将被停止。如果你在解码时间上进行统计，请记住这一点（如不的SRC / video_parser / vpar_synchro.c）。如果p_input> b_pace_control == 0，不要调用这个。
   input_Seek ( input_thread_t * p_input, off_t i_position ):改变阅读的偏移量，用于在一个文件跳转到另一个地方的情况。如果p_input->stream.b_seekable == 0，不能使用这个功能。该位置是一个在p_input - > p_selected_area - > i_start和p_input - > p_selected_area-> i_size（当前值p_input - > p_selected_area - > i_tell中）之间的一个数（通常是很长很长，取决于你的libc）。

####1.4.2注意

多媒体文件可以是非常大的，特别是当我们读取如/ dev / dvd的数据时，所以偏移必须是64位大。在很多系统，诸如 FreeBSD, off_t 是64位的可能会出错，但在GNU libc 2.x情况又不同了， 这也是为什么我们要使用-D_FILE_OFFSET_BITS=64 -D__USE_UNIX98编译VLC代码。

####1.4.3逃离流的不连续性

随意改变读取的位置会导致一个比较混乱的流，和解码器的读取错误。为了避免这点，我们发送多个NULL数据包（即包中没有包含什么，只是零），然后再改变阅读位置。事实上，在大多数的视频和音频格式下，一个时间足够长的零的流是一个可逃脱的序列，解码器可以很简单地退出。
*  input_OffsetToTime ( input_thread_t * p_input, char * psz_buffer, off_t i_offset ) : 将偏移量的值转换到一个时间坐标（用于界面显示）
*  input_ChangeES ( input_thread_t * p_input, es_descriptor_t * p_es, u8 i_cat ) : 取消选择所有类型i_cat和选择p_es的基本流。例如更改语言或字幕轨道。
*  input_ToggleES ( input_thread_t * p_input, es_descriptor_t * p_es, boolean_t b_select ) : 这是一个很简单的方式来选择或取消选择一个特定的接口基本流。
 Buffers management
输入插件必须用一种方式来分配和释放数据包（其结构将在下一章阐述）。基本上，我们需要四个功能：
*  pf_new_packet ( void * p_private_data, size_t i_buffer_size ) :分配一个新data_packet_t，和缓冲的i_buffer_size字节相关联的。
*  pf_new_pes ( void * p_private_data ) :分配一个新pes_packet_t。
*  pf_delete_packet ( void * p_private_data, data_packet_t * p_data )  :释放P_DATA。
*  pf_delete_pes ( void * p_private_data, pes_packet_t * p_pes ) :释放p_pes。
所有的功能都将p_input - > p_method_data作为第一个参数，这样就可以保持记录的分配和释放的数据包。

###1.5缓冲区管理策略

缓冲区管理可以有三种方式：

*  1.传统的libc的分配：对于我们已经使用很长一段时间的PS插件的malloc（）和自由（），我们需要每次分配或释放一个数据包。

*  2.网表：在这个方法中，我们分配了一个非常大的缓冲区开头的问题，然后管理的指针免费包（以下简称“网表”）的列表。这效果很好，如果所有的数据包具有相同的大小。它是用来长的TS输入。 DVD插件也使用它，但，因为缓冲区（2048字节）之间可以共享多个数据包添加一个refcount标志。它现在已经废弃，并不会被记录。

*  3.缓冲区高速缓存：目前，我们正在开发一种新的方法。它已经在使用的PS插件。我们的想法是调用malloc（）和free（），吸收流的违规行为，但重新使用一个缓存系统，通过所有已分配的缓冲区。我们正在扩大它，以便它可以被用于任何插件没有性能上的损失。 


###1.6解复用流

在正在阅读的pf_read，您的插件必须给一个函数指针的解复用器的功能。解复用器是负责解析数据包，收集PES和feeding解码器。标准MPEG结构的多路解复用器（PS和TS）已经被写入。您只需要表明input_DemuxPS和input_DemuxTS pf_demux的。你也可以写你自己的解复用器。
本文件的目的不是描述不同层次的在MPEG流的封装。具体请参阅您的MPEG规范。


















   




A
A
    
