cture_t  

主要的数据框架都存放在picture_t,描述了音频解码器所需要的一切，请参阅这些文件的详细信息。通常，P_DATA将是一个指向YUV平面图片。

###1.1.2 subpictree_t 和SPU

请注意subpicture_t的结构。其实该VLC SPU（子图像单元）解码器只解析SPU头文件，SPU的的图形数据转换成内部格式，可以呈现快得多。因此，“实际”的SPU解码器的一部分，主要是在的SRC / video_output/ video_spu.c

###1.1.3 vout_thread_t  


vout_thread_t结构复杂很多，但你不需要明白一切。基本上，视频输出线程管理堆的画面subpictures（默认情况下）。每个图片都有一个状态（显示，销毁，空...），并最终显示时间。视频输出的主要工作是一个无限循环 
 
1.在堆中发现下一张图片

2.当前子画面显示

3.如果视频输出不支持YUV覆盖，渲染将调用优化YUV插件，这也将缩放，添加字幕，和一个可选的图像信息领域

4.到达指定日期

5.显示图片。对于显示的RGB数据输出，它往往是用缓冲液交换来。 p_vout-> p_buffer是一个数组的两个缓冲器的YUV变换发生，并且p_vout-> i_buffer_index表示当前显示缓冲。

6.控制事件

##1.2 视频解码器所使用的方法

视频输出的堆的功能，使解码器可以将其解码后的数据输出。最重要的功能是由视频解码器指示的大小分配画面缓冲器vout_CreatePicture。然后，它只是需要（void *）p_picture-> P_DATA解码的数据后，调用vout_DisplayPicturevout_DatePicture。

picture_t*vout_CreatePicture（vout_thread_t*p_vout，IntI_TYPE，INTi_width，inti_height）：返回一个分配图片缓冲。 I_TYPE将实例YUV_420_PICTURE，i_widthi_height以像素为单位。

警告：

如果没有图片是在堆中，vout_CreatePicture将返回NULL。

vout_LinkPicture（vout_thread_t p_vout，picture_t* p_pic）：增加引用计数的图片，因此，它并没有得到意外释放，而解码器仍然需要它输出。比如，一个I或P图像可以仍然在显示交织B图像进行输出。  

vout_UnlinkPicture（vout_thread_t p_vout，picture_t* p_pic）：减小引用计数的图片输出。取消链接必须做的每一个环节输出。

vout_DatePicture（vout_thread_t p_vout，picture_t* p_pic）：提供该图片演示日期输出。您就可以开始工作在什么时候它会显示在图片输出。对于最新的I或P图片，你必须等待，直到你已经破译以前所有的B帧输出。

subpicture_t* vout_CreateSubPicture（vout_thread_t* p_vout，inti_channel，I_TYPE）：返回一个分配子图像缓存器输出。 i_channel是子图像信的ID，I_TYPE DVD_SUBPICTURE或TEXT_SUBPICTURE i_size是该数据包长度（以字节为单位）输出。

vout_DisplaySubPicture（vout_thread_t p_vout，subpicture_t* p_subpic）：告诉子画面已经将视频输出完全解码。它淘汰了以前子画面的输出。
vout_DestroySubPicture（vout_thread_t p_vout，subpicture_t* p_subpic）：将子图标记为空。

##1.3 如何写一个视频输出插件

视频输出需要考虑到系统调用，图像显示和管理的输出窗口输出。在vmem.c，有最简约框架，这只是“render”虚拟的内部存储器输出。从那里到directfb.csvgalib.c，，最后去X11和Windows输出。

视频输出主要在模块video_output  

modules/video_output/x11/xcommon.c提供写的功能 
  
intActive（vlc_object_t* p_this）对任何VLC模块，此功能验证模块是否适合VLC的核心需求，通过询问p_this结构输出。       

 在成功的情况下，激活设置回调函数运行所需的视频输出（所需的功能在下面解释），并返回VLC_SUCCESS

在失败的情况下，激活释放内存，并返回一个错误代码（VLC_EGENERIC，VLC_ENOMEM，...）
void Deactivate ( vlc_object_t *p_this )被称为破坏模块，取消需要释放所有分配的内存并销毁视频输出线程。

你需要实现回调函数：

*  (p_vout->pf_init, static int InitVideo ( vout_thread_t * );)调用开始输出线程，每一次调整窗口的大小，它创建了一个缓冲的输出画面

*  (p_vout->pf_end, static void EndVideo ( vout_thread_t * );) 销毁图像

*  (p_vout->pf_manage, static int ManageVideo ( vout_thread_t * );) 管理X11事件，并对窗口大小调整

*  (p_vout->pf_render, static void RenderVideo ( vout_thread_t *, picture_t * );) 用于从解码器显示图像

* (p_vout->pf_display, static void DisplayVideo ( vout_thread_t *, picture_t * );) 图片是否实际显示到屏幕上

*  p_vout->pf_control, static int Control ( vout_thread_t *, int, va_list );) 控制设备的视频输出

##1.4 如何写一个YUV插件

看C源代码的plugins/ YUV / transforms_yuv.c。你需要重新定义相同转换输出。基本上，它是一个矩阵乘法运算输出。













  
 










