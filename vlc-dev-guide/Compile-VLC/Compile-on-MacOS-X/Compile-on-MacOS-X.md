##<center>OSX编译方法</center>


* 1[先决条件](#1)
	* 1.1[苹果软件](#11)
	* 1.2[Xcode中选择Xcode4](#12)
	* 1.3[Git](#13)
	* 1.4[环境配置](#14)

* 2[获取源代码](#2 )
* 3[命令行编译VLC](#3)
* 4[组建步骤](#4)
    * 4.1  [其他开发工具](#41)
    * 4.2  [SDK 的选择 和 32/64位](#42)
		* 4.2.1 [SDK 的选择](#421)
		* 4.2.2 [32/64位的选择](#422)
    * 4.3  [准备第三方库](#code)
		* 4.3.1 [预建库（推荐）](#431)
		* 4.3.2 [组建自己的库（不适合菜鸟）](#432)
		* 4.3.3 [SDK 的选择](#421)
	* 4.4 [引导VLC](#44)
	* 4.5 [配置VLC的组建](#45)
	* 4.6 [编译VLC](#422)
	* 4.7 [为Mac打包成VLC应用程序](#47)
	* 4.8 [为Mac注册VLC应用程序](#48)
*  5 [故障排除](#5)
	* 5.1 [Xcode 路径](#51)
	* 5.2 [Xcode 版本](#52)
    * 5.3  [第三方库和路径](#53)
    * 5.4  [QTsound编译X.5](#54)
    * 5.5  [从X.5交叉编译 PPC](#55)
    	* 5.5.1  [先决条件](#551)
    	* 5.5.2  [GNU AS](#552)


* * *

<h2 id="1">先决条件</h2>
---------

<h3 id="11">苹果软件</h3>
* 你至少需要苹果系统版本 MacOS 10.5 但是，强烈建议使用 10.6 Snow Leopard或更高版本。

* 苹果开发工具可以从此处下载：[http://developer.apple.com/technology/xcode.html](http://developer.apple.com/technology/xcode.html)  
Both Xcode3 and Xcode4 should be fine.  
注意：如果使用Xcode4.3或更高版本，，必须通过手动的方式安装的命令行工具。此外，Xcode4.3 系统将会改变VLC的构建系统，目前正在等待和可能需要的补丁，直到问题的解决。

<h3 id="12">Xcode中选择Xcode4.3</h3>

如果在Xcode 4.3之前没有安装过Xcode的其他版本，你可能需要运行Xcode 命令，来选择你的 Xcode 开发的目录。

>`$ xcrun clang `

如果出现错误提示：'Error: No developer directory...',这时候需要使用Xcode选择 Xcode包所在的开发目录。
就像：

>`$ sudo /usr/bin/xcode-select -switch /Applications/Xcode.app/Contents/Developer `

<h3 id="13">Git</h3>

如果你安装的是Xcode 4.3 ，并且Git 已经安装完成，你仅仅是将你的终端指向它就可以了：

>`$ export PATH=/Developer/usr/bin:$PATH
`

如果你安装的是Xcode3 ，[Get Git from their Website](http://git-scm.com/)

<h3 id="14">环境配置</h3>

在Mac OS X 10.6 系统。在其最新版本上，VLC需要使用苹果的LLVM-GCC4.2编译器进行编译。为了使用这个编译器，你需要导出相应的变量。在Bourne shell中，键入（如果Xcode是安装到默认位置，bash是OS X默认的shell）：

>`$ export CC=/Developer/usr/bin/llvm-gcc-4.2  
$ export CXX=/Developer/usr/bin/llvm-g++-4.2  
$ export OBJC=/Developer/usr/bin/llvm-gcc-4.2  
`

在Mac OSX 10.8.2 上，使用下面方式：

>`$ export CC=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc  
$ export CXX=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++  
$ export OBJC=/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc   
`
如果您使用的是 C-Shell ，你当然要使用 setenv 命令了。


<h2 id="2">获取源代码</h2>
-----

>` $ git clone git://git.videolan.org/vlc.git
`
<h2 id="3">命令行编译VLC</h2>
------

>创建一个组件文件夹：

>` $ cd vlc && mkdir build && cd build
`

>运行组件命令：

>`$ ../extras/package/macosx/build.sh
`
>等待组件过程结束就完成了。

>你会看到很多对于组件过程的选项（改变 arch 或者 SDK）。

>`$ ../extras/package/macosx/build.sh -h
`

<h2 id="4">组建步骤</h2>
--------

现在，如果你愿意，你可以阅读下面的详细信息学习如何编译程序：

<h3 id="41">其他开发工具</h3>

你需要开发工具，尤其是正确编译ＶＬＣ所需要的所有的 autotools 。

这样做：

　　`$ cd vlc/extras/tools　 　 　 　 
`

　　`$ ./bootstrap && make　　 　 　  　 　 　 
`

　　`$ cd ../..`

关键：设置新的变量

>`$ export PATH=$PWD/extras/tools/build/bin:$PATH
`

<h3 id="42">SDK 的选择 和 32/64位 </h3>


<h4 id="421">SDK 的选择</h4>

如果你使用SDK 10.6 ，（你的VLC只能运行在10.6以及以上版本的计算机系统中 ）。

>`$ export OSX_VERSION=10.6
`

对于10.5版本，你同样可以达到相同的效果，但是你必须检查在你的 /Developer/SDKs/ 目录下已经安装MacOSX 10.5 SDk 。如果你是用的是 Xcode4.2 ，你可以安装 10.5 的SDK。

<h4 id="422">32/64位的选择</h4>

下面的内容将在10.6 (Snow Leopard) SDK的基础上编译生成一个64位的二进制。这是通过使用主机和x86_64-apple-darwin10生成变量显示的。

这就是以“三重”为架构的苹果系统。

ARCHITECTURE

* x86_64 represents Intel 64bits. 
* i686 represents Intel 32bits. 
* powerpc represents PowerPC 32bits

SDK SYSTEM

* darwin9 represents MacOSX 10.5. 
* darwin10 represents MacOSX 10.6. 

所以，为了能在 PowerPC 编译，你应该使用 powerpc-apple-darwin9。为了使 10.5 及以上能在 intel32 上成功编译，你应该使用 i686-apple-darwin9，为了使10.6及以上在intel64上成功编译，你应该使用 x86_64-apple-darwin10. 

<h3 id="43">准备第三方库</h3>

在编译 VLC 之前，你需要很多的库函数，下面是如何获得他们：

>` $ cd contrib  
 $ mkdir -p osx && cd osx  
 $ ../bootstrap --host=x86_64-apple-darwin10 --build=x86_64-apple-darwin10
`
<h4 id="431">预建库（推荐）</h4>

如果你想下载一个已经于组建好的包括所有必须库的源码包：

>`$ make prebuilt
`

然后跳转到[这个页面](http://wiki.videolan.org/OSXCompile#Bootstrap_VLC)进行引导

<h4 id="432">组建自己的库（不适合菜鸟）</h4>

如果你想从源代码直接进行组建编译：

>` $ make -j4 .gettext  
 $ export PATH=$PWD/../x86_64-apple-darwin10/bin:$PATH
`
然后：

>`$ make -j4`

如果没有错误提示，那么第三方库全部编译成功。你就可以进行下一步了。

<h4 id="433">返回</h4>

返回到VLC 根目录：

>`$ cd ../..`

<h3 id="44">引导VLC </h3>

这将会创建配置的脚本：

>`$ ./bootstrap`

<h3 id="45">配置VLC的组建 </h3>

创建文件夹：

>` $ mkdir -p build && cd build
`
列出configure 命令的不同选项：

`$ ../extras/package/macosx/configure.sh --help
`

组建64位二进制包：

>` $ ../extras/package/macosx/configure.sh --enable-debug --host=x86_64-apple-darwin10 --build=x86_64-apple-darwin10
`
<h3 id="46">编译VLC  </h3>

只需要下面的命令：

>`$ make -j4`

稍等片刻……

<h3 id="47">为Mac打包成VLC应用程序 </h3>

如果你想与其他用户或另一台计算机共享这个应用程序：

>` $ make VLC.app
`

如果你想创建一个镜像文件：

>` $ make package-macosx
`

可以为Safari/Mozilla 浏览器创建插件：`make package-macosx-plugin`

<h3 id="48">为Mac注册VLC应用程序 </h3>

如果你想拥有对此应用程序签名的证书，例如 Gatekeeper，你需要运行：

>` $ extras/package/macosx/codesign.sh -i "certificate name"
`

如果你想支持OS X Snow Leopard和Leopard的签名，你需要启用“-g”选项。请注意，您需要更换自己的签名叶哈希“75GAHG3SZQ”内的协同设计脚本之前这样做，因为您的证书将混合使用VideoLAN，由OS二进制文件将会被操作系统拒绝。



<h2 id="5">故障排除</h2>
-----


<h3 id="51">Xcode 路径</h3>

使用 Leopard, Xcode 需要以管理员的身份安装在自定义位置。虽然这对于普通的Xcode 工程项目没有任何问题，但是VLC 还需要一点小小的改动。你需要在 /Developer 目录下放置额外的连接，用来指向那些文件：

>`usr, Headers, Private, SDKs, Tools, Makefiles `

您可以轻松地为这些文件夹创建链接（theFolder是这六种类型之一）通过执行下面的命令：

>`ln -s /full/path/to/Developer/theFolder /Developer/theFolder
`

<h3 id="52">Xcode 版本</h3>

请确保您采用最新的Xcode3的或最新版本的Xcode4编译VLC

<h3 id="53">第三方库和路径</h3>

请特别注意，消除任何第三方包对您的计算机环境的影响。避免你的包管理器（自制软件，芬克，使用MacPorts）和contrib包管理器的冲突是很重要的。，我们用它来编译我们的资源。

这虽然不是必需的，但是他有可能发生。

Git 仍然可以被访问。

>`$ unset PKG_CONFIG_PATH  
$ unset PKG_CONFIG_LIBDIR  
$ export PATH=$PWD/build/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin
`

<h3 id="54">QTsound编译X.5</h3>

MacOS的X.5.SDK 损坏 - 2个解决方案

方案1 ：

* 下载MacOS10.6 sdk 从/Developer/SDKs/MacOSX10.6.sdk/System/Library/Frameworks/QTKit.framework/Headers/获得QTCaptureDecompressedAudioOutput.h 将他移动到 /Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/QTKit.framework/Headers/ 
* 编辑 /Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/QTKit.framework/Headers/QTKit.h并添加以下内容：  
`#import <QTKit/QTCaptureDecompressedAudioOutput.h> where needed.
`

方案2 ：

* 配置VLC构建使用MacOS10.6.sdk，通过添加以下标志：

`--with-macosx-sdk=/Developer/SDKs/MacOSX10.6.sdk
`

<h3 id="55">从X.5交叉编译 PPC</h3>

如果你想在X.6intel基础上为PPC 编译ＶＬＣ，你需要调整一些东西，因为苹果把它损坏了。

这是很先进的东西！

<h4 id="551">先决条件</h4>

确保：
>* have X.6.8 
* Xcode 4.2 installed in the normal /Developers location 
* Xcode 3 installed in /Xcode3 location 
* MacOS X.6 and X.5 SDK installed in /Developers/SDKs/ , as explained above (SDK selection).


 <h4 id="551">GNU AS </h4>

使用这个将不会有效果，因为PPC 的AS 在默认安装情况下已经损坏了。下面是如何修正它：

>`$cd /usr/libexec/as  
$ sudo mkdir ppc  
$ cd ppc  
$ sudo ln -sf /Xcode3/usr/bin/as as
`
　　

>>>>[Categories](http://wiki.videolan.org/Special:Categories): [Building](http://wiki.videolan.org/Category:Building) | [Coding](http://wiki.videolan.org/Category:Coding)
