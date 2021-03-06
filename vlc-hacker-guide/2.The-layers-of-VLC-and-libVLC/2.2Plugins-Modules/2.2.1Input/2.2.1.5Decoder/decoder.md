#解码器
===============================================================
 
##1怎样写一个解码器插件
       
###1.1在vlc中什么是一个解码器

解码器的过程中发挥了流的数学部分。它是从解复用器（在输入模块中）分离而来，并输出的线程，管理重建连续的基本流的数据包，这需要重组，解码器的样品，播放它们分离。基本上，一个解码器没有互动的装置，它是纯粹的算法。

在下一节中，我们将介绍如何从输入流解码器检索。输出API（怎么说“这个样本进行解码，可以播放在xx”）将在接下来的章节中谈到。

###1.2：解码器配置

输入线程从src/input/ decoder.c产生相应的解码器模块。

CreateDecoder（input_thread_t* p_input，es_format_t FMT，i_object_type）函数创建一个p_dec的变量的类型i_object_type（VLC_OBJECT_DECODER），然后调用module_Need（vlc_object_t* p_this，为const char* psz_capability，为const char* psz_name，bool b_strict）与* psz_capability=“decoder”和* psz_name=“$decoder”。 module_Need，用于生成一个列表。作为一个例子，我们可以看到，在a52的模块：   
 
  set_capability( "decoder", 100 );

这意味着当我们请求一个解码器，它的得分是100。在同一系统中使用的每个部分的VLC选择将使用哪个模块。然后，验证，如果解码器需要分组的数据（在这种情况下，它找到并加载打包器模块）。最终，它会启动解码器通过调用线程：

vlc_thread_create( p_dec, "decoder", DecoderThread, i_priority, false ) 
     
###1.3：数据包结构

输入模块提供了一个先进的流数据传送到解码器的API。首先让我们来看看在数据包结构。它们被包括在/input_ext dec.h。

data_packet_t包含一个指针的数据的物理位置。从解码器开始，直到p_payload_end在调用p_payload_start。此后，p_next如果它不为NULL它会切换到下一个数据包

b_discard_payload，如果该数据包的内容被弄乱，应该将其丢弃。data_packet_t是包含到pes_packet_t中。

pes_packet_t设有已链接的列表（p_first）的data_packet_t代表（在MPEG范式）一个完整的PES数据分组。对于PS流，通常只有一个pes_packet_t含有1 data_packet_t的

虽然在TS流，一个PES可以有几十的TS数据分组之间的分割。PES包的PTS日期（见MPEG规范的更多信息）和当前的阅读速度为插值时间（i_rate），应适用。 b_data_alignment（如果可用的系统层中）表示，如果该数据包是随机存取点，b_discontinuity告诉前面的数据包是否已被丢弃。         

在节目流中，一个PES数据分组设有仅一个数据包，其缓冲区包含PS标题，PES的首部，和数据有效负载。
在传输流PES包传输流中，一个PES数据分组可以设有无限数量的数据包（图中3个），其缓冲区包含PS标题，PES的首部，和数据有效负载。
     
 共享的同时在输入和解码器的结构是decoder_fifo_t。它设有一个旋转的FIFO的PES数据包，以被解码。输入提供了宏来操纵 

DECODER_FIFO_ISEMPTY，DECODER_FIFO_ISFULL，DECODER_FIFO_START，DECODER_FIFO_INCSTART，DECODER_FIFO_END，DECODER_FIFO_INCEND。请记得采取p_decoder_fifo - > data_lock的任何操作之前的FIFO。
 
要被解码的下一个数据包是DECODER_FIFO_START（* p_decoder_fifo）。当它结束后，你需要调用p_decoder_fifo - > pf_delete_pes（p_decoder_fifo - > p_packets_mgt，DECODER_FIFO_START（* p_decoder_fifo）），然后DECODER_FIFO_INCSTART（* p_decoder_fifo）返回PES缓冲区管理器。

如果FIFO是空（DECODER_FIFO_ISEMPTY）的，你可以阻止，直到一个新的数据包被接收链表的信号：vlc_cond_wait（＆p_fifo - > data_wait，p_fifo - > data_lock）的。你必须持有该锁在进入此功能之前。如果该文件是超过或用户退出，p_fifo-> b_die将被设置为1。这表明，你必须尽快释放所有的数据结构和调用vlc_thread_exit（）。

但是，这种传统的方式读取信息包是不是方便，因为可以任意分裂基本流。输入模块提供原语，使阅读更容易读取比特流。无论您使用的是您的选择，或者其他，但如果你使用它，你不应该访问数据包缓冲区。

该位的流允许你只是调用GetBits，（），此功能将透明地读取数据包缓冲区，改变数据包和PES包在必要时，你不得干预。因此，它是更方便您读取连续的基本流，你不必处理数据包边界和FIFO的比特流会为你做。

 其中心思想是介绍32位的缓冲区[正常WORD_TYPE，但64位版本不还，bit_fifo_t的。它包含的字缓冲和重要的位（较高的部分）的数目。输入模块提供5个内联函数管理

*  U32 GetBits（bit_stream_t p_bit_stream，无符号整数i_bits的）：返回下一个i_bits，位位缓冲器。如果没有足够多的位，它提取的以下从decoder_fifo_t字。此功能只保证24位。它的工作原理，直到31位的时刻，但它是一个副作用。我们不得不编写不同的功能，GetBits32，为32位读数。
 *  RemoveBits（bit_stream_t p_bit_stream，无符号整数i_bits）：为GetBits（），不同的是位不能返回（我们花几分钟的CPU周期）。它具有相同的限制，我们还写了RemoveBits32。

*  U32 ShowBits（bit_stream_t p_bit_stream，无符号整数i_bits）：为GetBits（），不同之处在于位不刷新看完之后，所以，你需要调用RemoveBits（）手之后。请注意，如果超过24位，此功能将无法正常工作，除非你有一个字节的边界上对齐（见下面的函数）。

*  RealignBits（bit_stream_t* p_bit_stream）：丢弃高位n位（<8），从而使缓冲器的第一个比特一个字节边界对齐。寻找对齐起始码（例如MPEG）时，它是有用的。    

*  GetChunk（bit_stream_t p_bit_stream，byte_t* p_buffer，为size_t i_buf_len;）：它是一个模拟的memcpy（）函数，但作为第一个参数比特流。必须分配和p_buffer，至少i_buf_len长。它是复制你想要的数据跟踪。

这些功能重新创建一个连续的基本流模式。当该位缓冲区是空的，他们采取的下列当前包中。当数据包是空的，它切换到下一data_packet_t的，或unapplicable的pes_packet_t（see p_bit_stream - > pf_next_data_packet）。所有这一切是完全透明的。

###1.4：输入模块  

####1.4.1包的变化和对齐问题


我们要研究的两个问题的结合。首先，data_packet_t可以具有偶数的字节数，例如177中，所以被截断的是最后一个字。其次，许多CPU（SPARC，α...）只能读取词语的一个字边界上对齐的（即，一个32位字的32位）。因此，数据包的变化是一个复杂的，你可以想像，因为我们要读取截断的话，必须得到对齐。

 例如GetBits（）将调用UnalignedGetBits（）从src /input/ input_ext.dec.c的。基本上，它会读取字节后的字节流，直到被重新调整。 UnalignedShowBits（）是一个比较复杂，一个临时包（p_bit_stream - > showbits_data）。

 要使用的比特流，你调用p_decoder_config， - > pf_init_bit_stream（bit_stream_t p_bit_stream，decoder_fifo_t p_fifo）设置的所有变量。你可能会需要经常从包中获取特定的信息，例如PTS。如果p_bit_stream - > pf_bit_stream_callback不为NULL，它会被称为一个数据包上的变化。见的SRC / video_parser/ video_parser.c的一个例子。第二个参数表示不仅仅是一个新的data_packet_t也是一个新的pes_packet_t。您可以将您自己的结构存放在p_bit_stream - > p_callback_arg。

####1.4.2 警告

当你调用pf_init_bit_stream，pf_bitstream_callback尚未定义，它会跳转到第一个数据包，虽然。你可能会想调用你的pf_init_bit_stream比特流的回调。

###1.5：内置的解码器

VLC已经设有一个MPEG的层1和2音频解码器，MPEG MP @ ML视频解码器，AC3解码器（借用铁青），一个DVD SPU解码器，和一个LPCM解码器。你可以写你自己的解码器，模拟视频分析器.  

####1.5.1 当前设计的限制


要添加新的解码器，你必须添加流类型，和src/input/ input_programs.cAA硬线连接的代码中。

MPEG音频解码器是本地的，但不支持第3层解码，AC3解码器是一个港口亚伦霍尔茨曼的libac3（原libac3是不可重入的），SPU的解码器是原生的。您可能会想，去看看在BitstreamCallback中的AC3解码器。在这种情况下，我们有跳前3个字节的PES数据包，这不是基本流的一部分。视频译码器的情况比较特殊，并且将在下面的部分中进行说明。

###1.6MPEG视频解码器


VLC媒体播放器提供的MPEG-1，MPEG-2主轮廓@ Main Level的解码器。它本身写的VLC，已经相当成熟。它的状态有点特殊，因为它是两个logicial实体：视频分析器和视频解码器之间劈裂。最初的目标是单独的比特流解析功能，高度并行化的数学算法。从理论上讲，可以是一个视频分析器线程，以及视频解码器线程，做几个街区的IDCT和补偿。 
  
它没有（也不会）支持MPEG-4或DivX解码。它不是一个编码器。它应该支持MPEG-2 MP @ ML规范，虽然一些功能仍留有未经检验的，如差分运动矢量。请记住前面，输入基本流必须是有效的（例如这是不是这种情况时，直接读取DVD多角度的vob文件）。

 最有趣的文件是vpar_synchro.c的。它解释了整个丢帧算法。简单地说，如果机器是足够强大的，我们的解码器，所有建设和平综合战略，都是有效的，否则，如果我们有足够的时间（这是基于解码时间统计）所有IP地址进行解码。另一个有趣的的文件是vpar_blocks.c，它描述了所有的块（包括系数和运动矢量）解析算法。在该文件的底部，我们的确产生一个优化的功能，每一个普通的图片类型，和一个缓慢的通用功能。也有几个层次的优化（这使得编译速度较慢，但​​某些类型的文件的速度更快解码）被称为VPAR_OPTIM_LEVEL，级别0表示没有优化，1级表示MPEG-1和MPEG-2帧图片的优化，第2级是指为MPEG优化-1和MPEG-2的场和帧图片。运动补偿插件（即复制的地区从参考图片）是非常依赖于平台（例如MMX或AltiVec技术的版本），所以我们把它的plugins /。这是更方便的视频解码器，也可以使用由其他的视频解码器（MPEG-4）得到的插件，插件必须确定6功能

*  vdec_MotionFieldField420， vdec_MotionField16x8420， 
*  vdec_MotionFieldDMV420， vdec_MotionFrameFrame420
*  vdec_MotionFrameField420，vdec_MotionFrameDMV420。

###1.7：IDCT插件    

就像IDCT是特定于平台的。所以我们把它移到插件/ IDCT。此模块IDCT的计算，将数据复制到最终的画面。您需要定义七种方法

*  vdec_IDCT（decoder_config_t p_config，dctelem_t p_block，INT）：完整的2-D IDCT。 64个系数是在p_block的。

*  2.>vdec_SparseIDCT（vdec_thread_t p_vdec，dctelem_tp_block，i_sparse_pos）：IDCT块上只有一个非NULL的系数（指定的i_sparse_pos的）。您可以使用定义的plugins / IDCT/ idct_common.c的的64矩阵在初始化时预先计算这些功能。   
*  3.vdec_InitIDCT（vdec_thread_t p_vdec）：，需要的vdec_SparseIDCT是否初始化的东西。    
*  4. vdec_NormScan（U8 ppi_scan[2][64]）：通常情况下，这个函数什么也不做。对于小规模的优化，一些IDCT（MMX）需要反转某些在MPEG扫描矩阵系数（见ISO / IEC13818-2）。   
*  5. vdec_InitDecode（vdec_thread_s* p_vdec）：初始化的的IDCT和可选作物表。    
*  6. vdec_DecodeMacroblockC（】结构vdec_thread_s p_vdec，结构macroblock_s* p_mb）：解码一个完整的宏块，其数据复制到最终的图片，包括色信息。     
*  7. vdec_DecodeMacroblockBW（vdec_thread_s* p_vdec，结构macroblock_s*p_mb）：整个宏块解码，其数据复制到最终的画面，除了色信息（在灰度模式下使用）。
 目前，我们已经实现了优化的版本：MMX，MMXEXT，和AltiVec不工作。我们有两个简单的C版本，正常（据说优化）的伯克利版本（idct.c）的，和简单的1-D分离IDCT从的ISO参考解码器（idctclassic.c“）。

###1.8对称多处理（SMP)

MPEG视频解码器VLC可以利用多个处理器上，如果必要的话。我们的想法是推出许多解码器，将几个宏块在一次执行IDCT。

管理池的功能是在的SRC / video_decoder/ vpar_pool.c。并不建议非SMP的机器上使用，因为它实际上是速度比单细丝版本慢。有时仅仅使在SMP机器上...