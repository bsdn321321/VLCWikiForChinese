M。不过，为了解决数字音频直通的需要，音频输出也可以接受编码的音频帧封装为S / PDIF数据包  
>>这说明了在VLC1.2.0版本中发现了第四个版本的音频输出层。 0.5.0到1.1.x的版本是基于一个部分类似，但不兼容的接口，被称为aout3  
>       
>2：写一个音频输出的模块
>>对于一般的读写模块的更多详细信息，请参阅文件：Haker guider的编写指南。音频输出模块应该用正确的功能和类别 如下声明：
>>>set_capability("audio output", 60)
>>>set_category(CAT_AUDIO)    
>>>set_subcategory(SUBCAT_AUDIO_AOUT)     
>>>set_callbacks(Open, Close)       
>>>（注：回调名称是不同的，我们使用open（）和close（）在这个例子中）。
 音频输出模块的实例存储自己的内部状态（如果有的话）作为一个aout_sys_t结构.        
>>>>struct aout_sys_t
{
    /* ... */
};                                      
 >>2.1 优先级                             
>>>除非以及配置好的特定的模块，或者通过AOUT命令行参数指定，LIbvlc将每个音频输出模块的优先级从高到底的顺序，直到成功。除非显示配置，否则常用的模块和0优先级永远不会被探测。      
>>>因此，例如在Linux的pulseaudio的模块具有比ALSA1更高的优先级，OSS模块具有最小的（非零）的优先级。文件的音频输出零优先事项，将不能正常使用。如果可用，让VLC使用PulseAudio，否则ALSA，否则OSS。
>
>3：初始化   
>>音频输出将探测和初始化典型的open（）回调。音频输出，应该检查输入音频格式       
audio_output_t.format      
static int Open (vlc_object_t *obj)      
{
    audio_output_t *aout = (audio_output_t *)obj;  
    aout_sys_t *sys;
    /* Check input format */  
    vlc_fourcc_t format = aout->format.i_format;     
    unsigned samplerate = aout->format.i_rate;      
    unsigned channels = aout_FormatNbChannels(&aout->format);            
    /* Initialize audio subsystem */    
    sys = malloc (sizeof (*sys));
    if (unlikely(sys == NULL))  
        return VLC_ENOMEM;
    /* ... */
    if (failure)
    {
        free (sys);
        return VLC_EGENERIC;
    }        
    /* Adjust format to stereo */
    aout->format.i_original_channels =
    aout->format.i_physical_channels = AOUT_CHAN_LEFT|AOUT_CHAN_RIGHT;
    /* aout->format.i_format = VLC_CODEC_S16N; */
    /* aout->format.i_rate = 48000; */       
    /* Setup callbacks */
    aout->sys = sys;
    aout->pf_play = Play;
    aout->pf_pause = Pause;
    aout->pf_flush = Flush;
    aout_VolumeSoftInit (aout);
    return VLC_SUCCESS;
}
>
>>当完成时，音频输出模块已经初始化
>>>static void Close (vlc_object_t *obj)         
{   
    audio_output_t *aout = (audio_output_t)obj;
    aout_sys_t *sys = aout->sys;                     
    /* Deinitialize */                             
    /* ... */      
    free (sys);
}

 >>3.1:音频格式
>>>当启动open(),最初的格式，通常是在桌面系统VLC_CODEC_FL32（浮点型），但不总是这样。所有格式都是隐式通道交错。从未使用过Uninterleaved？音频。例如，立体声音频如下：    
      1.第一左声道                      
      2.第一右声道               
      3.第二左声道                     
      4.第二右声道               
      .等等
>>>目前，格式如下：         
VLC_CODEC_FL32 	Single precision 	float 	Native 	With FPU 	Allowed
VLC_CODEC_FI32 	Fixed-point 	int32_t 	Native 	Without FPU 	Forbidden
VLC_CODEC_S16N 	Signed 16-bits 	int16_t 	Native 	Without FPU 	Allowed
VLC_CODEC_F32L 	Single precision 	float 	Little 	With little endian FPU 	Allowed
VLC_CODEC_F32B 	Single precision 	float 	Big 	With big endian FPU 	Allowed
VLC_CODEC_F64L 	Double precision 	double 	Little 	Never 	Allowed
VLC_CODEC_F64B 	Double precision 	double 	Big 	Never 	Allowed
VLC_CODEC_S16L 	Signed 16-bits 	int16_t 	Little 	Without FPU 	Allowed
VLC_CODEC_S16B 	Signed 16-bits 	int16_t 	Big 	Without FPU 	Allowed
VLC_CODEC_S24L 	Signed 24-bits 	N/A 	Little 	Never 	Allowed
VLC_CODEC_S24B 	Signed 24-bits 	N/A 	Big 	Never 	Allowed
VLC_CODEC_S32L 	Signed 32-bits 	int32_t 	Little 	Never 	Allowed
VLC_CODEC_S32B 	Signed 32-bits 	int32_t 	Big 	Never 	Allowed
VLC_CODEC_A52 	AC-3 / Dolby 	Non-linear 	N/A 	A52 input 	Forbidden
VLC_CODEC_DTS 	DTS Coherent Acoustics 	Non-linear 	N/A 	DTS input 	Forbidden
VLC_CODEC_MPGA 	MPEG 2 Audio 	Non-linear 	N/A 	MPEG input 	Forbidden
VLC_CODEC_SPDIFL 	S/PDIF 	uint16_t 	Little 	Never 	Allowed (S/PDIF)
VLC_CODEC_SPDIFB 	S/PDIF 	uint16_t 	Big 	Never 	Allowed (S/PDIF)     
在on ertry”一栏显示在什么情况下（如有），格式可以由LibVLC核心的音频输出open()回调。“on return”列决定，是否得到实际输出的格式支持.      
    如果从一个指定的LibVLC核心在入境时，返回的格式不同，LibVLC自动插入任何所需的转换过滤器。所以，不要手动转换输出模块.   
>>>3.1.1 S/PD/F    
当且仅当进入的格式非线性的，音频输出模块可以启用数字直通模式。要做到这一点，它必须设定音频输出格式到VLC_CODEC_SPDIFL（或VLC_CODEC_SPDIFB）。如果相反直通是不被使用，则格式必须被设置为一个线性FOURCC，通常VLC_CODEC_FL32或VLC_CODEC_S16N。   
  >>>3.1.2 别名    
>>>>VLC_CODEC_FL32是根据架构的endianess VLC_CODEC_F32L或VLC_CODEC_F32B的别名。为方便完整列表本地字节序FOURCC
1 VLC_CODEC_FL32 (float)
2 VLC_CODEC_FL64 (double)
3 VLC_CODEC_S32N (int32_t)
4 VLC_CODEC_S24N (N/A)
5 VLC_CODEC_S16N (int16_t)
6 VLC_CODEC_U16N (uint16_t)   
>>3.2 采样率和信道   
>>>采样率是来自解码器或音频过滤的采样率，所以是信道的映射。
如果可能的话，它建议的音频输出尽可能靠近输入使用的格式。这是为了转换和质量损失。然而，由于硬件的限制我们常常需要使用不同的输出格式： - 再采样aout是否已被 - > format.i_rate修改， - 再混合的通道如果aout已-> format.i_physical_channels和/or aout已被修改-> format.i_original_channels - 则转换样本格式AOUT-format.i_format已经被修改        
>>3.3 警告
>>> 要注意的是直到返回VLC_SUCCESS（0），Open（）回调不能改变的AOUT->格式。如果要改变格式，然后再返回初始化失败，模块将得到腐败信息的输入。

>>4:播放 
>>>实施的audio_output_t.pf_play回调是强制性的。 LibVLC核心将一次调用回调音频数据块：
>>>static void Play (audio_output_t *aout, block_t *block)   
 { 
 const void *data = block->p_buffer; /* Pointer to audio data */    
    size_t datalen = block->i_buffer; /* Byte size of audio data */    
    unsigned samples = block->i_nb_samples; /* Number of samples in the  block */    
    /* NOTE: For linear formats:
      datalen = samples * channels * aout_FormatBitsPerSample(&aout->format) */  
        /* Queue the block in some platform-speific buffer */
    /* ... */   
    block_Release (block); /* release memory */
}  
一个音频数据块中的样本数依赖于特定音频解码器，输入格式。它也可能由某些音频过滤器改变。
在上面的例子中，该块同步被破坏，但是这不是强制的。 block_Release（）的线程是安全的。如果您需要保留音频数据时间，你可以异步调用block_Release（）。     
>>4.1 同步   
>>>每个存储块有一个时间戳和一个持续时间。在大多数情况下，时间戳等于前块的时间戳和前块的长度的总和。时间戳和持续时间用微秒表示。如果采样率不是一个除数为1000000，LibVLC核心会自动调整长度，舍入误差不会导致长期漂移。   
   /* Time the sample should be physically rendered: */           
    mtime_t pts = block->i_pts;                 
    /* Current time */                          
    mtime_t now = mdate();                       
    /* Block duration */                         
    mtime_t length = block->i_length;            
    /* Estimate hardware latency */
    /* ... /            
    /* Report timing to LibVLC core */              
    aout_TimeReport (aout, block->i_pts - latency);                     

>>>音频输出模块负责同步。 aout_TimeReport（）通知LibVLC当前时间的音频输出有效。延时值必须从底层音频子系统获得;报告的时间上采样或下采样如果不同步超过一定阈，则在子系统上细节会有所不同。这种情况通常发生在音频硬件时钟和输入媒体计时没有完全一致的时钟速率。使用（aout_TimeReport）是可选的。一些音频输出模块实现自己的机制，以弥补不同步
 。Pulseaudio（声音服务器）的输出模块要求pulseaudio的服务器，而不是重新取。不关心时间同步所有文件输出模块。       
 >>>然而，对于真实音频输出，绝对需要某种形式的同步。没有它，就没有唇同步播放视频。因此声音输出接口，无需任何机制来估计避免延迟（例如，SDL音频）
>  
>5：暂停    
>>在暂停播放时，音频输出需要通知，以便它可以尽快设为静音。为此目的，音频输出模块应提供audio_output_t.pf_pause回调
static void Pause (audio_output_t *aout, bool pause, mtime_t pts)     
{      
    if (pause)   
    {                                                         
        /* Pause playback immediately */     
    }     
    else      
    {
        /* Resume playback from where it was paused previously */ 
    }
}
                     
>>这个回调是可选的，可以为NULL。如果暂停没有完成，音频播放将继续直到底层的音频缓冲区欠载。这听起来业余的特别是当使用大缓存的缓冲区（VLC1.2允许2秒）。     
>>5.1 参数  
>>>LibVLC核心认为暂停布尔参数总是被切换。它始终认为第一次暂停（）被调用时，总是真的 ，第二次等，总是假的。当暂停RO重新被触发时，它应该是在最近的过去与就该对mdate（）。
>       
>>5.2 注意                               
>>>当恢复输入播放暂停状态发生，这是完全无关的暂停和/或暴露的一些硬件的电源管理功能。音频输出模块负责电源管理自己的内部
>   
>6.清空/排除    
>>停止播放的时候，应尽快丢弃音频缓存区。相反的，当达到结束时，音频的缓冲器必须被排出，以避免裁剪。处理这个的的可选audio_output_t.pf_flush回调      
static void Flush (audio_output_t *aout, bool wait)           
{                         
    if (wait)                 
    {
        /* Wait for buffers to be drained */            
    }          
    else           
    {
        /* Flush (discard) buffers */            
    }
}
>     
>7：容量管理   
>>根据底层子系统的能力上，LibVLC提供三种模式的体积（扩增）
>>>软件体积/放大：LibVLC的核心适用于在内部进行。   
>>>硬件音量/放大：音频输出适用于以任何方式相应的的音量。   
>>>没有量/放大   
对于S / PDIF直通，软件体积显然是不支持的。
音频输出模块需要选择正确的的卷管理模式中的Open（）回调。它应该调用以下功能之一：
aout_VolumeSoftInit（AOUT）为LibVLC软件的音量，
“硬件”的量，     
aout_VolumeHardInit（AOUT，VolumeSet）
aout_VolumeNoneInit（AOUT）关闭卷     
>> 7.1 硬件体积   
当硬件模式选择libvlc，将回调改变体积
static void VolumeSet(audio_output_t *aout, float volume, bool muted)        
{   
    / * ...*/    
}     
>>>如果体积修改，音频输入将能够修正。aout_VolumeHardSet(aout, volume, muted);     
 >>>7.1.1 静音    
>>>>从量的的静音标志是独立。这使得UI从保存的音量电平分开静音控制。 
>    
>8：输出设备的选择
>>8.1 在音频播放时，用户界面将寻找“音频设备”的VLC对象变量的audio_output_t对象来保存当前的输出设备和可输出设备的。如果该变量不存在，接着选择音频设备将显示为灰色。运行时间

>>8.2 配置 
>>>对于持久性设置，音频不工作，一个正常的配置项应该在插件描述符中声明。通常，名称是“XXX音频设备”，其中XXX是输出模块的名称，例如：为ALSA
  add_string ("alsa-audio-device", "default", N_("ALSA device"), NULL, false)        change_string_list (alsa_devices, alsa_devices_text, NULL)      
>>>但是，如果相关子系统提供了它自己的（每个应用程序）的设置，对于PulseAudio的情况下，不应该有任何持久的配置项。这将是redumdant。
