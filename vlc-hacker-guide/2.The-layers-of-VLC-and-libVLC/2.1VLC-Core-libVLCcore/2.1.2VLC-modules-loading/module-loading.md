<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
#Vlc加载模块的方法#
>1.模块的介绍
>>Vlc有一个核心和大约200到400个模块。没有这些模块vlc不能工作，因为这些模块提供了我们所期待的各种功能。
>>>vlc模块包括两个主要部分：
>>>>VLC_MODULE_CAPABILITY：描述模块的范畴.   
>>>>VLC_MODULE_SCORE模块的核心.   
>
>2.怎样安装模块
当你第一次安装模块的时候，你可以看到一些默认的插件，这些插件包括vlc的模块以及缓存插件，所以这些模块可以快速的运行。模块有顺序的存放在指定的目录下。
>
>>最新的vlc版本需要特定的模块否则不会安装成功。模块必须以以下格式命名： libmodule_name_plugin.ext 。Module_name 应该是你小模块 的名字。Ext是系统共享区域的扩展。例如：win 下，进入http模块的名字是 libaccess_http_plugin.dll
>>当vlc需要一个模块的时候，它接受命令，打开一个有高可能的模块。
例子:当vlc 需要解码器的时候，它打开解码器的模块，直到执行。
它以递减的顺序打开，然后运行open()功能模块，当一个模块运行成功，vlc运行这个模块。
>
>3：关于模块加载的高级信息
>>分数为0
>>>如果一个模块存在很多0，他需要由用户或者vlc自动加载。
All ，none,and other speial tweaks
>
>1.All意味着所有 的模块以递减的顺序检测。   
>2.None意味着没有模块将被检测。    
>任何模块都可以运行，利用它的别名。这个对0分模块有用。
例如：
>模块要求可以被限制。例
--codec avcodec,alltry the avcodec module than all modules as a "decoder"    
--demux avformat,none try the avformat module and no other module       
>模块请求默认是all 模式的，以及all模式也可以被删除。         
>怎样将模块加入列表：   
Useing console
vlc --list       
用gui        
Menu -> Tools -> Plugins and extensions
##模块的主要内容##
>1.audio filter: an audio filter, like an equalizer音频过滤器，就像一个均衡器一样。
>2.audio mixer: an audio channel mixer, like a downmixer音频频道变换，就像音响。
>3.audio output: an audio output, like Windows DirectX audio output音频输出。
>4.decoder: a codec decoder, like theora解码器。   
>5.demux: a demuxer, to open a file format, like mkv分路器。  
>6.encoder: a codec encoder, like x264编码器。  
>7.interface: an interface, like the Qt interface接口。  
>8.meta reader: a meta reader, to read metadata读取源信息。     
>9.packetizer: a packetizer打包 .   
>10.playlist export: a module to write playlist, like .m3u列表输出  .
>11.services_discovery: a module to get extra content from your +computer or the network, like Upnp, DLNA网络服务 .   
>12.sout access: an access for the streaming信号的访问 .   
>13.sout mux: a muxer when streaming and encoding信号复用器 .   
>14.stream_filter: a stream filter流过滤器 .   
>15.text renderer: a way to display subtitles and other text on top of the video输出字幕以及其他文本信息. 
>16.video filter: a video filter, like contrast adjusting视频过滤器 .  
>17.visualization2: a visualizer, to create videos from the music可视化。        
>18.vout display: a video output, to display videos like Direct3D or Xv   Direct3D or Xv的形式输出视频。  
