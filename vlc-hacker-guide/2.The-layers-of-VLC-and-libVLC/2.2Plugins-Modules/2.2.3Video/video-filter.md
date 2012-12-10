#视频过滤器

##在源代码树中的位置，编译

 video filters的正确位置是在 modules/video_filter/ folder中。
 
 ##说明
 

在modules/video_filter/Modules.am看video filters在VLC中的列表。新的集成模块上提供更多的关于如何将一个新的模块构建系统的帮助。

 

##编程惯例和技巧media player video filters通常是在C99上编写的，剩余的使用 C++，例如AtmoLight plugin.


平常的东西在这里也拥有：

1.在没有bug的条件下，使用assert（）检查条件。

2。不要使用assert（）检查stuff，因为可能会导致运行失败。

3.保持代码的可读性

4.如果可能的话，每行最大不超过80个字符。特别是对于视频滤镜：

请记住，这是低层次的东西，需要快速。

1.速度有多快？请注意，源可能是交错的，有人可能会抛出倍帧率到过滤器链.这意味着，对于60i信号，对每个输出帧解码，整个需要大约16毫秒。

2.保持所需的内存带宽下降

     （1）除非有必要，否则不要复制所有的图片，因为进行那样的操作很花费时间。

      (2）分配一个输出图像和直接渲染到它

      (3)如果你需要一个以上的通道，如果可能的话，就进行in-place处理。

     （4）如果您的处理不能避免多遍，可考虑在一点时间内做一列图片的传递（或几个），而不是遍历整个图片用于每个传递。这将有助于减少CPU缓存的压力（因为一些图片可能适合的L2高速缓存）。

3.考虑编写矢量化的内联汇编，如MMX内循环处理。而能获得2-8X的速度的一个因素，取决于需要多少和什么样的处理算法。

##视频过滤器API的一些注意事项
   注意：请参阅modules/ video_filter/deinterlace/ deinterlace.c和modules/ video_filter/deinterlace/ deinterlace.h的例子。

  视频过滤器使用基于对象的模型。过滤器的调用将产生一个实例的指针，所以每个过滤器实例可以保持本地数据。一般，每一个过滤器定义其自己的内部数据结构被称作filter_sys_t。这完全是私人性质的过滤器。视频过滤器VLC1.2的API被称为视频过滤器2。这需要函数open（）和Close（）。

Open（）函数可以分配私有数据（如果有的话），并设置过滤器结构的指针，帧处理函数（p_filter - > pf_video_filter，这是实际的过滤器），冲洗功能（p_filter - > pf_video_flush的），和一个鼠标事件的功能（p_filter-> pf_video_mouse）。相关类型定义在include / vlc_filter.h中。

Close（）函数释放的应该是私人数据。

鼠标功能能产生鼠标事件，从滤波器的输入格式（注意方向！）到滤波器的输出格式。这在必要时可以进行缩放或几何失真，从而使鼠标的位置正确映射。请参阅/ vlc_filter.h的定义和Mouse（）在modules/ video_filter/deinterlace/ deinterlace.c的一个例子。如果你不需要重新映射鼠标事件，你可以离开p_filter - > pf_video_mouse，其值为NULL。

###筛选工作（帧处理功能）

帧处理功能需要的帧作为输入（picture_t*，包括/ vlc_picture.h的），和任选的一个或多个帧（picture_t*）输出作为一个链接的列表。通常的情况下是一帧，一帧的输出。 （请参阅在反隔行扫描模块的帧速率倍增器和IVTC）。

   如果你不希望通过一个特定的呼叫处理功能输出帧，您可以返回NULL。如果你想输出数的链表，可以通过使用p_next成员picture_t实现。

   你不必一定输出相同的帧（后处理），你可以在您的filter_sys_t中保留一个私有的输入框历史，并调整PTSs（介绍时间戳输出，在picture_t的member）。反隔行扫描提供了一个如何做到这一点的例子。

   但是请注意，有可能是其他的过滤器链中已经设置了的帧偏移，这留下更少的时间（直到指定PTS）用于其余部分的过滤器执行其它处理。
picture_Release( p_inpic );

###帧分配
 
确保分配输出的照片

    picture_t *p_outpic = filter_NewPicture( p_filter );

  此功能是从一个的私有pool（见的SRC / video_output/ vout_wrapper.c）请求新图片。这是非常重要的！请注意，图片这样创建：

    picture_t *p_temp = picture_NewFromFormat( &p_input_pic->format );

  缺乏共享内存上下文（在Linux或等值的其他OS），因此不能被传递到视频输出的逻辑。如果你的过滤器试图这样做，VLC会崩溃。

  如果你需要临时的图片，你可以分配使用picture_NewFromFormat（），但请记住，创建输出图片使用filter_NewPicture（）。

  同时在private的picture可用插槽的数量有一定限制。目前（[71992c5fbc75ee2c94cd2a3ab1aaca70bfc688a9]），这是3张图片的过滤层。请参阅在SRC / video_output/ vout_wrapper.c的private_picture。如果您尝试分配更多的输出图像（在一个单一的处理调用），分配将失败。

注意：

  在VLC1.2，视频格式（分辨率，色度）是不会在fly改变。整个过滤链是关闭的（）D，如果更改格式，再次open()。

  请注意，它被允许冲洗过滤器而不关闭它。实际上，这在某些情况下是可能发生的，所以不要在您的冲洗功能释放东西。相反，动态资源分配中的open（），并释放他们中的Close（）。参考如何写一个模块。

  每个过滤器支持不同的输入和输出格式。通常都支持YUV格式，例如
I420，J420，YV12，I422，J422。参考include/ vlc_fourcc.h，最重要的是I420和I422。

###间距和可见的间距

  重要的东西：

       *  i_pitch = number of (macro)pixels on one line
       *  i_visible_pitch = number of (macro)pixels on one line, adjusted for memory alignment constraints etc. (see below) 

  请注意每个plane的图片可能不同,同时在YUV formats里边的亮度(Y_PLANE)和色度(U_PLANE, V_PLANE)由于色度抽样会有不同的picture(In 4:2:0 formats, the number of lines differs, too.)  

  即使画面的大小一样，Pitches往往也会稍微有所差异，这取决于画面的分配方式。到过滤器的输入图象可能有一个间距在临时图片（picture_NewFromFormat（）），和输出画面（filter_NewPicture（））之间。

  当你处理的像素的图片，一定要始终使用正确的间距。也就是说，始终使用你工作的i_pitch member of the actual plane_t 。

  如果你确实需要匹配pitch（例如，如果你是粘合在处理代码从另一个GPL兼容的项目，假设这一点，你不想把它改写...），考虑制作临时副本与picture_NewFromFormat（）。参考modules/video_filter/deinterlace/deinterlace.c (the history mechanism pp_history[])和modules/video_filter/deinterlace/algo_yadif.c 的使用。

  如果您正在处理的像素从一个画面到另一个安全的事情是占用最小的i_visible_pitch的，并从x = 0的循环，直到可见的间距已经达到了，但必须使用单独的i_pitches计算像素的位置。

Video_format_t vs. Plane_t 

  在video_format_t中, i_visible_width和i_visible_height的members是和i_x_offset还有i_y_offset的是关联的，但是和lane_t:: i_visible_*是没有联系的。

  如果想要哪部分的存储器平面可以被显示，那么就需要查看plane_t::i_visible_* fields。一般这些都是不同于由于内存对齐约束的整个表面，他们通常不会改变对一个给定的的图片指针（但他们可以改变的，例如在Direct3D缓冲区）。

  video_format_t:i_visible_width/height和i_x/y_offset更多的是一个'hint'用于决定什么才会被实际播放。如果需要的话，filter需要更新 filter_t::fmt_out的值，以确保分配到的picture得到正确的值。然而，过滤器不应改限制其处理这一领域，因为VLC支持动态裁剪。

  因此，在过滤器中做的正确的事情是根据plane_ts处理整个图像区域，或至少所述第一条i_visible_*线和像素。过滤器不需要关心margin的定位或存在，即使存在这样的事情作为margins. 
  
关于建立和合并图片

  本节讨论有关如何创建过滤器，创建和合并已经存在的视频到顶部的图片。

  1.picture_t和subpicture_t的不同点

  （1）一个picture_t是一个完整的形象，通常是解码后的视频帧。

  （2）subpicture_t是一个可以被覆盖的元素（准确的说，一个元素列表的图像的顶部）。存在两种类型的元素：文本和图像。文本元素在呈现前被VLC core所覆盖。

  2.如何创建一个图片，并将其与现有的图片合并

   （1）Code-wise是创建一个视频类型子图源过滤器（VLC2.0）的最简单的方法。一个子图像源的任务是建立一个subpicture_t，然后让该VLCcore在视频流的顶部处理它。

   （2）另一种方法是产生一个picture_t，然后自己进行处理。

  注意：在VLC追至2.0 的版本中(version 1.1和其以下的)，subpicture sources被称为subpicture filters.该视频滤波器类型已被重新命名，以便允许产生子画面过滤器，用于编辑现有的subpicture_ts。  


关于写一个filter的最简单的例子

   在modules/video_filter/和sub source目录中可以找到这样的filter.值得一提的例子包括：

     modules/video_filter/logo.c：在视频的头部进行图像的叠加。请注意，这也实现了​​picture_t的视频过滤器2的直接编译。所以这可能不是最简单的来源。如果你想采取这种方式，参考the deinterlace filter。


    modules/video_filter/marq.c：在视频的头部进行文本的叠加
    

    modules/video_filter/rss.c：在视频的叠加一个来自于一个RSS stream的文本。这其中也包括图片元素。有时这使得它一个很好的例子去了解如何复合subpicture_t的元素。

