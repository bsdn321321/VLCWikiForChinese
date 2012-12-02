##<center> Win32编译方法</center>


* 1[组建方法](#BuildingMethods)

* 2[获取工具链](#Obtainingtoolchain )
    * 2.1  [编译器和二进制工具](#21)
    * 2.2  [开发工具](#22)
    * 2.3  [主机类型](#23)
*  3 [获取源代码](#getsource)
*  4 [进入VLC目录](#gotodir)
*  5 [准备第三方库](#prepare3rd)
    * 5.1  [64位linux](#51)
    * 5.2  [修复contrib路径](#52)
    * 5.3  [返回到VLC目录](#53)
*  6 [配置编译环境](#compilecinfig)
    * 6.1  [自动引导](#61)
    * 6.2  [配置](#62)
*  7 [组建VLC](#buildvlc)
*  8[打包VLC](#packaging)

* * *

<h2 id="BuildingMethods">组建方法</h2>
---------

>如果你想从源代码编译VLC ，有以下几种方式供你选择：在linux上用Mingw交叉编译，包含工具链  首选的方法（使用交叉编译）。在Windows上，你应该在虚拟机中完成。
MSYS+ MinGW的本机编译  使用MSys编译   本机的编译方法。 在Microsoft Windows下，MSYS是一个编译Unixish项目的很小的编译环境。
使用cygwin本机编译   用Cygwin编译    建立使用cygwin的编译环境，容易出错、而且速度很慢

<h2 id="Obtainingtoolchain">获取工具链</h2>
-----
>友情提示：以下仅适用于linux的交叉编译

<h3 id="21">编译器和二进制工具</h3>

>为了在Windows（32位或者64位系统）上编译VLC源代码，我们需要 Mingw-w64 工具。

*   debian/ubuntu :执行命令  apt-get install gcc-mingw-w64-i686
(在ubuntu上你必须首先在wheezy和above上找到这些包)
VLC的2.0.x及以下版本使用的是旧版的mingw32 工具，它仅支持32位windows系统，如果你使用mingw-w64 有问题的话，你可以尝试使用mingw32代替：
*   Debian/Ubuntu: 执行命令 apt-get install gcc-mingw32 mingw32-binutils. 

>需要注意的是mingw32的版本至少为3.17debian是不会提供的，你可以在此获取[mingw32-runtime-3.17](http://people.videolan.org/~jb/debian/mingw32-runtime_3.17.0-0videolan_all.deb)

* Gentoo 用户可以 emerge crossdev && crossdev mingw32 
* ArchLinux 用户可以 pacman -S mingw32-gcc 
* Fedora 用户应该阅读 [Win32 Compile UnderFedora](http://www.wikivideolan.org) 
* 其他 Linux 系统应该尝试这里 [http://www.mingw.org/wiki/ LinuxCrossMinGW](http://www.mingw.org/wiki/LinuxCrossMinGW) 
*  使用 MSYS+MINGW 本机编译, 应该阅读手册 [documentation](http://wiki.videolan.org/Win32CompileMSYSNew) 
* 使用 Cygwin 本机编译, 应该阅读手册 [documentation](http://wiki.videolan.org/Win32CompileCygwinNew) 


<h3 id="22">开发工具</h3>
>你应该需要以下：

* lua5.1
* 所有的autotools ：libtool /automake,autoconf,autopoint,make,gettext
* git
* pkg-config
* subvision
* 如果你想重新组建所有的贡献，还需要cmake,cvs
* zip (创建.zip包)，p7zip [创建.7z包]，niss[对.exe文件自动安装]，bzip2 [用于预生成]

###
<h3 id="23">主机类型</h3>
>下面的一些命令示例中包括工具链的标识。这个值是必不可少的：它指示建立的系统，在Windows下正确的使用工具和编译程序的。如果没有该值时，系统将为Linux下执行一个本地编译（或任何能在您的计算机上运行的）。一个不正确的值，构建就会失败

>这是被称为主机类型，虽然在使用 Mingw 情况下是更重要的一对。确切的值取决于你安装的工具。值得注意的是，在Debian / Ubuntu，这些值必须使用：

* i686-w64-mingw32 for Windows 32-bits, using the Mingw-w64 toolchain 
* x86_64-w64-mingw32 for Windows 64-bits, using the Mingw-w64 toolchain 
* i586-mingw32msvc for Windows 32-bits, using the Mingw32 toolchain 

再一次强调，你必须在下面的命令段中替换一些值

<h2 id="getsource">获取源代码</h2>
---
`$ git clone git://git.videolan.org/vlc.git vlc
`

See [Git](htps://wiki.videolan.org/Git) for more information.

<h2 id="gotodir">进入VLC目录</h2>
---
`
$ cd vlc
`

<h2 id="prepare3rd">准备第三方库</h2>
---

在编译VLC之前，你需要很多其他的函数库，这里展示如何获得它们：

`$ mkdir -p contrib/win32`

 `$ cd contrib/win32`

`$ ../bootstrap --host=i586-mingw32msvc` 

 `$ make prebuilt`

如果你想自己重新组建所有人贡献的函数库，你有足够的冒险精神、有足够的时间的话：

`# apt-get install subversion yasm cvs cmake
`

`$ mkdir -p contrib/win32`
 `$ cd contrib/win32`

` $ ../bootstrap --host=i586-mingw32msvc`

` $ make fetch`

` $ make`

<h3 id="51">linux 64-bit</h3>
如果你是64位linux系统，那么你应该删除一些文件，或者安装 lib32 安装包(ia32-libs, multilibs, etc...) 

` $ rm -f ../i586-mingw32msvc/bin/moc ../i586-mingw32msvc/bin/uic ../i586-mingw32msvc/bin/rcc
`

除此之外，安装 `qt4-tools` 包

<h3 id="32">修复您的contrib路径</h3>
如果你的 Mingw prefix 不是 i586-mingw32msvc (你不是在 Debian /Ubuntu), 那么需要创建一个符号链接来贡献。 

`$ ln -sf ../i586-mingw32msvc ../i486-mingw32
`
<h3 id="53">返回到VLC源代码目录</h3>


`$ cd -`

<h2 id="compilecinfig">配置编译环境</h2>
---

<h3 id="61">自动引导</h3>

首先，准备生成树结构

`$ ./bootstrap`

<h3 id="62">配置</h3>
现在你可以使用 ./configure 脚本对编译环境进行配置了
创建一个子文件夹
`$ mkdir win32 && cd win32
`
使用标准的配置
`$ ../extras/package/win32/configure.sh --host=i586-mingw32msvc
`
友情提示：使用你的 Xcompiling 前缀，就像 `i486-mingw32 `

或者，您可以手动运行配置：

`$ ../configure --host=i586-mingw32msvc
`

请查看 '../configure --help' 获取更多帮助信息

<h2 id="buildvlc">组建VLC</h2>
---

如果你配置成功的话，运行以下命令来组建VLC：

` $ make`

<h2 id="packaging"> 打包VLC</h2>
------
一旦编译完成后，你就可以建立基于本机的VLC包，使用以下`make rules`：


<table border=1>
<tr border=1>
<td width=40%>命令</td>
<td width=60%>描述</td>
</tr>
<tr>
<td>make package-win-common</td>
<td>创建一个包含所有二进制代码的文件名为 vlc-x.x.x 的文件。你可以直接在目录下运行VLC程序。 </td>
</tr>
<tr>
<td>make package-win-strip (might be package-win32-strip) 
</td>
<td>同上，但是它不包含二进制代码(也就是说, 它占用最小的空间、并且不能使用调试器). 
</td>
</tr>
<tr>
<td>make package-win32-7zip 
</td>
<td>
同上，但是它会打包成 7z 格式的文件.
</td>
</tr>
<tr>
<td>make package-win32-zip 
</td>
<td>同上， 但是它会打包成 zip 格式的文件. 
</td>
</tr>
<tr>
<td>make package-win32 
</td>
<td>同上，但是它会产生一个自动安装文件，你必须在默认的路径下已经对这个工程安装过 NSIS 。 
</td>
</tr>
</table>

至此，你已经完成了VLC的编译了！Good Luck ！

[Category](http://wiki.videolan.org/Special:Categories)：[Building](http://wiki.videolan.org/Category:Building)

