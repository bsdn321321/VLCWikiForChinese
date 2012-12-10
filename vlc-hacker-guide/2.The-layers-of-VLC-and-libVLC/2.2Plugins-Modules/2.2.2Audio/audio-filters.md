n audio filter

*  模块描述符

 

static int Open     ( vlc_object_t *p_this );

static void Close    ( vlc_object_t *p_this );

static void DoWork   ( aout_instance_t *p_aout, aout_filter_t *p_filter, aout_buffer_t *p_in_buf, aout_buffer_t *p_out_buf );

 

vlc_module_begin()

   set_description( N_("audio filter x") )

   set_shortname( N_("audio filter x") )

   set_category( CAT_AUDIO )

   set_subcategory( SUBCAT_AUDIO_AFILTER )

   add_shortcut( "afx" )

   set_capability( "audio filter", 0 )

   set_callbacks( Open, Close )

vlc_module_end()

*  强制性结构

aout_filter_sys_t

*  I / O缓冲器

  数据进和出一次在aout_buffer_t中的模块，一个样本中的插件，在每个样品中，由通道形成一个block。

data stream
	

ch 1
	

ch 2
	

ch 1
	

ch 2
	

ch 1
	

ch 2
	

...

 
	

Sample 1
	

Sample 2
	

Sample 3
	

...

音频过滤器模块由一个aconstructor, a destructor, 和 p_filter->pf_do_work function组成，构造函数被一个p_filter传递构，如果它能够做整体在p_filter - >input和p_filter->output之间的转换，则输出0. 如果你能做到只有部分的改造，说你不能做到这一点（如果AOUT核心没有找到一个合适的过滤器，它会分裂的改造，并再次问你）。

 

*  注意：

Audio filters由三部分组成：

Converters : change i_format (for instance from float32 to s16).

Resamplers : change i_rate (for instance from 48 kHz to 44.1 kHz).

Channel mixers : change i_physical_channels/i_original_channels (for instance from 5.1 to stereo).

音频过滤器还可以任意组合这些类型的。例如，你可以有一个变换A/525.1FLOAT32立体声音频过滤器。该构造函数还必须设置p_filter - > b_in_place的。如果是0，AOUT核心将分配一个新的缓冲区的输出。如果是1，当你写一个输出缓冲区中的字节，它破坏了相同的字节输入缓冲区中（它们共享相同的内存区域）。一些过滤器可以工作，因为他们只是做一个线性变换（如FLOAT32 - >S16），但是大多数过滤器将要b_in_place= 0。该过滤器可分配私有数据p_filter - > p_sys。不要忘了释放它的析构函数。p_filter-> pf_do_work得到作为参数的一个输入和一个输出缓冲器，并处理它们。在处理结束，由于它们不是aout core,不要忘记设置p_out_buf - > i_nb_samples和p_out_buf - >i_nb_bytes(它们的在输入和输出之间的值可以改变)

#编写一个音频混合器

写一个音频混频器和写一个音频滤波器是非常类似的。唯一的区别是，你必须自己处理输入缓冲器，当你有需求时，请求新的缓冲区。在和pf_do_work的两个通话时，其在缓冲区中的位置被记录在p_input->p_first_byte_to_mix。（由于输入和输出缓冲器可以有不同的长度，所以它并不总是开始的缓冲区）。
