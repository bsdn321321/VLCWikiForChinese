##<center>源码结构树</center>

* 1.[VLC Source tree](#31)
* 2.[Modules source tree](#32)
* 3.[VLC Preferences](http://wiki.videolan.org/index.php?title=Documentation:Hacker%27s_Guide/Preferences&action=edit&redlink=1)
* 4.[VLC Plalist and Media Library](http://wiki.videolan.org/index.php?title=Documentation:Hacker%27s_Guide/Playlist&action=edit&redlink=1)
<br/>
<br/>
<br/>
<br/>



---
<h3 id="31">VLC Source tree</h3>
---
>本页将描述VLC代码的代码树的使用指南.随着VLC的发展,想完全了解VLC也是比较困难的.当你看见一种新代码时,你可能会被着众多的目录吓坏的,因此这个页面就是解决这种情况的.

<table border=1>
<tr>
<td>目录名称</td>
<td>目录解释</td>
</tr>

<tr>
<td>bindings</td>
<td>Java,CIL和Python bindings</td>
</tr>

<tr>
<td>contrib</td>
<td>所需的库文件(含makefile自动下载(或编译)的文件和补丁),配置时请先尝试预编译开发版头文件</td>
</tr>

<tr>
<td>doc</td>
<td>文档(可能不是最新的)</td>
</tr>

<tr>
<td>include</td>
<td>包含VLC的头文件</td>
</tr>

<tr>
<td>libs</td>
<td>包含装载机(在linux上加载win32的dmo代码),和SRTP的一个库</td>
</tr>

<tr>
<td>M4</td>
<td>automak 和 autoconf 所需要的宏文件</td>
</tr>

<tr>
<td>Modules</td>
<td>最重要的是src文件夹,<a href="">去src代码树看看</a></td>
</tr>

<tr>
<td>po</td>
<td>18种软件语言文件</td>
</tr>

<tr>
<td>projects</td>
<td>基于libvlc的插件,Mozilla插件,Active插件和MacOS X框架等</td>
</tr>

<tr>
<td>share</td>
<td>包含图标，以及软件的默认设置等</td>
</tr>

<tr>
<td>src</td>
<td>仅次于Modules最重要的模块，<a href="">去src代码树看看</a></td>
</tr>

<tr>
<td>test</td>
<td>软件测试脚本</td>
</tr>
</table>

##其他##
<table border=1>
<tr>
<td>extras/analyser</td>
<td>包含一些有风格的代码编辑器(vim,emacs)的宏,以及一些valgrind的方案</td>
</tr>

<tr>
<td>extras/buildsystem</td>
<td>包含alternative buildsystems</td>
</tr>

<tr>
<td>extras/deprecated</td>
<td>包含一些暂时不用的文件</td>
</tr>

<tr>
<td>extras/misc</td>
<td>包含类型不符的文件</td>
</tr>

<tr>
<td>extras/package</td>
<td>包含一些特殊文件,如:ipkg,rpm,win32,mac os 的安装文件</td>
</tr>
</table>
<br>
<br>
<br>
<br>

---
<h3 id="32">Modules source tree</h3>
---
>这个页面描述了modules中树形结构,目的在于给初学者一个代码概述以下目录将按字母顺序列出,右边是他们的释义.<br>
**注意**：本注释并不完全,只列出插件子目录,如果其在父目录中除并非很重要,否则不再强调.如果你需要一个全面的vlc插件列表,请[点击](http://trac.videolan.org/vlc/browser/trunk/modules/LIST)
<table border=1>
<tr>
<td>目录名称</td>
<td>子目录名称</td>
<td>目录解释</td>
</tr>

<tr>
<td>access</td>
<td>&nbsp;&nbsp;</td>
<td>通过网络协议(http,ftp,fake,tcp,udp等)访问访问如cd和dvd的媒体</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>cdda</td>
<td>cd音频读取模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>dshow</td>
<td>windows下directshow访问encoding plugin</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>dvd</td>
<td>调用v412 api的DVB-S/C/T 输入模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>MMS</td>
<td>MMS通过tcp,udp和http协议进入模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>rtsp</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>screen</td>
<td>截取主屏幕</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>vcd</td>
<td>光盘访问模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>vcdx</td>
<td>以导航形式访问光盘</td>
</tr>

<tr>
<td>access-filter</td>
<td>&nbnsp;&nbsp;</td>
<td>包括timeshift,record,dump的过滤器,他们用处?</td>
</tr>

<tr>
<td>access-output</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>audio-filter</td>
<td>&nbsp;&nbsp;</td>
<td>各种音频过滤器,如解码器,均衡器,转换器等</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>channel-mixer</td>
<td>各种混合器和解码器如Dolby解码器</td>
</tr>


<tr>
<td>&nbsp;&nbsp;</td>
<td>converter</td>
<td>固定或浮点格式的音频转换成 AC/3 或者MPEG I-II 1,2,3音频层</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>resamler</td>
<td>音频重采样</td>
</tr>

<tr>
<td>audio-mixer</td>
<td>&nbsp;&nbsp;</td>
<td>混合器插件</td>
</tr>

<tr>
<td>audio-output</td>
<td>&nbsp;&nbsp;</td>
<td>音频输出插件如ALSA,OSS,和DirectX audio</td>
</tr>

<tr>
<td>codec</td>
<td>&nbsp;&nbsp;</td>
<td>该目录包括各种解码器,尤其是ffmpeg可以用于编码和解码各种格式</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>cmml</td>
<td>媒体标记语言注释,解析超链接</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>dmo</td>
<td>DirectMediaObject的译码器,用于DirectMedia视频解码(wmv3)</td>

<tr>
<td>&nbsp;&nbsp;</td>
<td>FFmpeg</td>
<td>视频解码器ffmpeg需要使用的库</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>spudec</td>
<td>RLE DVD字幕解码器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>xvmc</td>
<td>xvmc视频输出解码器</td>
</tr>

<tr>
<td>cotrol</td>
<td>&nbsp;&nbsp;</td>
<td>播放器控制接口:手势,热键,歌词,远程控制,远程登录</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>http</td>
<td>http方式远程控制webinterface</td>
</tr>

<tr>
<td>demux</td>
<td>&nbsp;&nbsp;</td>
<td>各种多路分配器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>asf</td>
<td>asf多路分配器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>avi</td>
<td>avi多路分配器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>mp4</td>
<td>MP4多路分配器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>mpeg</td>
<td>mpeg分配器</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>playlist</td>
<td>播放列表导入模块</td>
</tr>

<tr>
<td>GUI</td>
<td>&nbbsp;&nbsp;</td>
<td>不同平台的GUI接口和各种头文件接口</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>beos</td>
<td>BeOS的音频输出,视频输出和界面模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>macos</td>
<td>MacOS的音频输出,和接口模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>pda</td>
<td>使用 Gtk2+的界面小部件合集</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>QNX</td>
<td>QNX操作系统插件</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>qt4</td>
<td>qt4界面模块所需库,随后的发布版将默认使用此界面</td>
</tr>
<tr>
<td>&nbsp;&nbsp;</td>
<td>skins2</td>
<td>新一代可更换界面</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>wince</td>
<td>掌上电脑界面</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>wxdidgets</td>
<td>wxwindows界面模块所需库,默认为VLC 0.86a 的界面</td>
</tr>

<tr>
<td>meta-engine</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>Misc</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>meta-engine</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>dummy</td>
<td>虚拟的(没有GUI时)音频输出,视频输出,界面和输入模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>memcpy</td>
<td>内存复制模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>notify</td>
<td>通知使用libnotify</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>plsylist</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>probe</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>testsuite</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>xml</td>
<td>libxml,xtag xml的解析</td>
</tr>

<tr>
<td>mux</td>
<td>Various Muxers</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>mpeg</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>RTP</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>packetizer</td>
<td>&nbsp;&nbsp;</td>
<td>H264/AVC MPRG 4的视音频流分包器</td>
</tr>

<tr>
<td>services-dicovery</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>stream-out</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>


<tr>
<td>&nbsp;&nbsp;</td>
<td>transrate</td>
<td>(速率转换)</td>
</tr>


<tr>
<td>video-chroma</td>
<td>&nbsp;&nbsp;</td>
<td>图相转换如YUV转换成RGB</td>
</tr>

<tr>
<td>video-filter</td>
<td>&nbsp;&nbsp;</td>
<td>反交错，变换，边界等各种视频过滤器</td>
</tr>

<tr>
<td>video-ouput</td>
<td>&nbsp;&nbsp;</td>
<td>&nbsp;&nbsp;</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>directX</td>
<td>使用direct3D,direct X的API的视频输出模块,还有windows中的opengl</td>
</tr>
<tr>
<td>&nbsp;&nbsp;</td>
<td>QTE</td>
<td>用于移植版qt的视频输出模块</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>X11</td>
<td>用于X11 API的视频输出模块</td>
</tr>

<tr>
<td>visualization</td>
<td>&nbsp;&nbsp;</td>
<td>一些可视化,包括goom</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>galaktos</td>
<td>一个可视化模块,输出opengl</td>
</tr>

<tr>
<td>&nbsp;&nbsp;</td>
<td>visual</td>
<td>可视化系统</td>
</tr>
</table>

请参阅:[VLC用户指南-第二章:VLC的模块和选项](http://www.videolan.org/doc/vlc-user-guide/en/ch02.html)
</body>