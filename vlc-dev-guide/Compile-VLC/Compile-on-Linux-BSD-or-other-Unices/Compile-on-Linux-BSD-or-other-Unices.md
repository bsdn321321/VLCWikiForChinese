##<center> Unix/linux编译方法</center>


* 1[准备开发环境](#BuildingMethods)

* 2[获取源代码](#Obtainingtoolchain )
* 3[获取第三方库]
    * 3.1  [建议方式](#31)
    * 3.2  [较差版本系统上的获取方法](#32)
    * 3.3  [防止你浪费时间的方法](#33)
	* 3.4  [任意使用其他库函数]
*  4 [配置](#getsource)
	* 4.1  [特殊库](#41)
	* 4.2  [最后的配置](#42)
	* 4.3  [Ubuntu](#43)
*  5 [编译](#gotodir)
*  6 [备注](#prepare3rd)
    * 6.1  [Cygwin](#61)
    * 6.2  [Debian/Ubuntu](#62)
*  7 [故障排除/常见问题](#compilecinfig)
    * 7.1  [Lua](#71)
    * 7.2  [XCB](#72)
	* 7.2  [Pull之后编译出错](#73)

* * *

<h2 id="BuildingMethods">准备开发环境</h2>
---------

>VLC需要一个C编译器，开发头文件和工具链。 gcc可以完成，但你也可以使用LLVM或intel专有C99/ C++编译器。
如果你是从Git 仓库获取源码来组建VLC，那么你还需要GNU的编译系统。也称之为“autotools”（autoconf,automake,libtool 和gettext 工具）来设置 makefile。你还要确保它们是最新的并且适用于您的操作系统。


>Fedora系统：

>`% sudo yum install git libtool pkg-config
`

>Debian/Ubuntu系统：

>`% sudo apt-get install git libtool build-essential pkg-config autoconf
`

>Arch系统：

>`% sudo pacman -S base-devel git pkg-config autoconf automake
`

<h2 id="Obtainingtoolchain">获取源代码</h2>
-----

从[获取源代码](http://wiki.videolan.org/GetTheSource)开始,使用FTP获取官网release版本。或者使用[GIT](http://wiki.videolan.org/Git)来跟进VLC的发展进度。

如果你是使用官方release版本，下载，加压缩之后会产生VLC的目录。例如：

>`% wget ftp://ftp.videolan.org/pub/videolan/vlc/2.0.4/vlc-2.0.4.tar.xz
`  
`% tar xvJf vlc-2.0.4.tar.xz
`  
`% cd vlc-2.0.4`


如果您使用的是Git的开发版本，那么要从启动引导源代码树开始：

>`% git clone git://git.videolan.org/vlc.git
`  
`% cd vlc
`   
`% ./bootstrap
`

如果 autotols 丢失或者是低版本的会导致自引导失败。






<h2 id="21">获取第三方库</h3>

-----------


>现在，你可以配置 VLC 的构建了。但首先，你需要确保所有需要依赖的选项都准备好。使用 ./ configure - help命令。你就会发现巨大的选项列表。

>安装并启用所有需要的第三方库是非常关键的。如果你想有一个完整的或者大部分功能的VLC构建，那么可能需要很多第三方库。如果你没有安装相关的库，那么你可能就会在某一个VLC应用上停止……基本上没有做任何有用的东西。查看完整列表，请参阅[这里](http://wiki.videolan.org/Contrib_Status)。

>非常重要的依赖关系:gettext(NLS）用于获得国际社会的支持（必需），libdvbpsi 用于MPEG-TS文件和流的支持，libmad 用于MP3音频解码，libmpeg2 用于MPEG1和MPEG2视频的支持，ffmpeg或者libav（libavcodec，libavformat，libpostproc，libswscale 和可选的libavio）用于MPEG4和大多数其他音频和视频编解码器，以及多种文件格式的liba52（AC3）的声音，dvdread和dvdnav，live555上DVD播放RTSP流播放等。


>对于音频输出，你可能需要的alsa-lib（在Linux上）和/或libpulse（pulseaudio的）。对于视频输出，你通常会需要XCB/ XVideo的和/或OpenGL/ GLX。和qt4需要得到的图形用户界面支持。

>需要注意的是，您需要安装VLC开发包（开发头文件和导入库）编译，而不仅仅是运行时。在Debian / Ubuntu中，以-dev结尾的正确的包名。在RPM的分布上，他们通常以-devel结尾。

>特别提醒：你的发行版如果有些库没有提供，你可能会更好静态连接VLC。但是，如果其他多媒体应用程序更新之后的版本，你可能会遇到很多问题。这是特别是在ffmpeg或者libav，live555上出现问题尤为突出。


有几种方法可以得到这些库。在同一时间，你只使用一个方法就足够了：

<h3 id="31">建议方式</h3>

为了获得所有必须的包，建议使用本机系统发行版本中的包或者 portage 系统。
在debian/Ubuntu上：

>`$ sudo apt-get build-dep vlc
`

openSUSE 用户需要看一下zypper手册中安装源（si）的相关说明。

>`$ sudo zypper si -d vlc
`
注意：要获得这些库，你必须首先添加VLC的资源库到你的系统中。

在openSUSE中：

>`$ sudo zypper ar http://download.videolan.org/pub/vlc/SuSE/<openSUSEversion> VLC
`
>你应更换<openSUSEversion>与您的系统（12.1，11.4，11.3，11.2或11.1版本的）相对应。

<h3 id="23">较差版本系统上的获取方法</h3>

>如果你的系统发行版不提供所需的库，或者你真正想要的将VLC静态链接，使用VLC贡献系统，它包含在该VLC源里面。

>首先，你需要安装GNU autotools（如果你还没有这样做），CMake，subversion，Git和最近的GNU / tar 实用程序或同类型的工具。

>`# apt-get install subversion yasm cvs cmake
`

>接下来运行命令: 

>`% cd contrib  
% mkdir native  
% cd native  
% ../bootstrap  
% make
`

>请注意上面的命令是VLC2.0或更高版本。详细旧版本略有不同：

>`% cd extras/contrib  
% ./bootstrap  
% make
`

这将会为你的系统下载安装很多库，不幸的是，人们组建VLC时候使用了大量的库和各种不同的平台，因此，这种方法只建议经验丰富的Unix开发者。

<h3 id="23">防止你浪费时间的方法</h3>

>阅读[列表](http://wiki.videolan.org/Contrib_Status)，下载VLC代码并用手工组建它们。

<h3 id="23">任意使用其他库函数</h3>

>有些时候，一些操作系统（OS）支持的函数库不包含必须的库，必须通过包系统安装它们。特别是 ALSA，PulseAudio 和 OpenGL。

<h2 id="">配置</h2>
-------

>./configure 是用来检查您的系统是否能够编译VLC,也可以选择你要组建的功能。作为提醒，这条命令可以有不同的参数选项。

>`% ./configure --help
`

>VLC 2.0 及以上版本:对于大多数用户, ./configure 不需要其他参数选项

>默认情况下，将会自动检测那些依赖与函数库的功能会被自动编译。如果首先被编译了，VLC也就会有那些功能。

>注意那些没有包含在默认编译的列表里的函数库，将不会出现在VLC资源库里面。我们必须知道pkg-config ,便于我们在./configure 里面找到他们。

>有一些功能默认情况下被禁用（不编译）。如果你想要他们，他们必须使用configure标志强制被编译，。你可以找到这些功能的列表，在./configure-help 找到为“disabled”的列表。

>(菜鸟指导: e输入命令：)

>`% ./configure --help | less
` 

>并按下回车键。键入一个斜杠“/”，类型为“disabled”（不带引号），按下回车键。按 n 键进入到下一个，N 去前面一个，q返回到命令行。使用向上/向下箭头键来滚动。 --cache-file 的选项（属于配置本身）之外的所有组合是VLC的功能，如果需要的话，一定选择他们）。

VLC1.1和更早的版本：您可能需要调整“configure”行。

<h3 id="23">特殊库</h3>

>VLC2.0及更高版本：有没有什么特别的库。 它会自动检测 live555里面的contrib/子目录。即不在默认的编译列表里的库，也不在VLC贡献的所有库里面，就必须知道pkg-config，用./ configure以找到他们。

>VLC1.1和更早版本：使用 --with-live555-path=path/to/livemedia/source/tree  in connection with --enable-live555 。对于 FFmpeg 或者 libav 。pkg-config 是vlc配置时找到相关函数库的惟一的方法，所以，如果你的FFmpeg/libav 库没有安装在默认的编译列表里面，或者你想使用讲台链接库，你需要正确的配置 环境变量 PKG_CONFIG_PATH  。

<h3 id="23">最后的配置</h3>

>如果你想把VLC安装在另外一个目录里面，运行：

>`% ./configure --prefix=/path/to/install/folder/
`

这是一个典型的VLC配置的一个例子：

>`% ./configure --enable-x11 --enable-xvideo --enable-sdl --enable-avcodec --enable-avformat \  
 --enable-swscale --enable-mad --enable-libdvbpsi --enable-a52 --enable-libmpeg2 --enable-dvdnav \  
 --enable-faad --enable-vorbis --enable-ogg --enable-theora --enable-faac --enable-mkv --enable-freetype \  
 --enable-fribidi --enable-speex --enable-flac --enable-live555 --with-live555-tree=/usr/lib/live \  
 --enable-caca --enable-skins --enable-skins2 --enable-alsa --enable-qt4 --enable-ncurses
`

[这里](http://wiki.videolan.org/User:J-b#VLC_configure_line)还有另一个. 

<h3 id="23">Ubuntu</h3>

>如果你在./configure后连续出现错误，并考虑重新安装相应的库。这将重新设置正确的路径和其他信息。检查$ PKG_CONFIG_PATH环境变量是否被设置为一个路径中的库像libavcodec.pc是否有效。否则，创建环境变量，将其导出，然后更新ldconfig。

<h3 id="23">编译</h3>

>编译VLC

>`% make`

>你不需要安装VLC来使用它，你也可以在组建目录下运行命令启动VLC：

>`# ./vlc`

>如果你确实想在你的系统里面安装VLC，可以运行：

>`# make install `

>过后你也可以卸载它，但是你又想保持原来所构建的树结构，你可以运行：

>`# make uninstall `

>要删除在编译期间（可选）创建的文件：

>`# make clean `

<h2 id="23">备注</h2>
---------

<h3 id="23">Cygwin</h3>

在Cygwin上编译可能会经常被经常变化的Cygwin包所破坏。我们建议从Linux到Windows的是交叉编译来代替。自己决定吧。

<h3 id="23">Debian/Ubuntu </h3>

>Debian用户如果想编译应该安装以下包：

>* [libavcodec-dev](http://packages.debian.org/unstable/libdevel/libavcodec-dev) 
* [libpostproc-dev](http://packages.debian.org/unstable/libdevel/libpostproc-dev)
* [libmpeg2-4-dev](http://packages.debian.org/unstable/libdevel/libmpeg2-4-dev)

如果你只是想使用VLC媒体播放器，那么只需VLC的安装包（sudo apt-get install vlc) 大多情况下不稳定的版本是最近发布的，而稳定的是比较旧的版本。

<h2 id="7">故障排除/常见问题</h2>
------

<h3 id="71">Lua</h3>

如果提示"LUA byte compiler missing." 表示你需要安装Lua。需要安装Luac ，lua字节编译器。

>在 Debian/Ubuntu: 

>`% sudo apt-get install lua5.1
`
>在 Fedora：

>`% sudo yum install lua
`

<h3 id="72">XCB</h3>

VLC1.1及更高版本要求XCB库处理与X11显示器。请勿禁用你的XCB否则你不会得到任何视频支持。

>要安装这些库运行以下命令（Debian / Ubuntu）

>`% sudo apt-get install libxcb-shm0-dev libxcb-xv0-dev libxcb-keysyms1-dev libxcb-randr0-dev libxcb-composite0-dev
`
>在  Fedora :

>`% sudo yum install libxcb-devel xcb-util-devel
`

>对于OpenGL（仅适用于Debian / Ubuntu），您将需要XCB额外的xlib ：

>`% sudo apt-get install libx11-xcb-dev
`

如果你的发行版提供了一个版本的Xlib没有XCB，那么这以后的包也不会提供的。因此，您将无法使用OpenGL。那就使用XVideo 代替吧。

<h3 id="23">Pull之后编译出错</h3>

代码源最后被 pull 之后， 好像是仓库中的代码发生了很显著的变化，并且之前的构建也已经过时了。怎么办呢？你可以在[模块指南](http://wiki.videolan.org/Hacker_Guide/How_To_Write_a_Module#Module_load_troubleshooting)中查看故障排除/常见问题的相关描述。

！Good Luck ！

[Category](http://wiki.videolan.org/Special:Categories)：[Building](http://wiki.videolan.org/Category:Building)

