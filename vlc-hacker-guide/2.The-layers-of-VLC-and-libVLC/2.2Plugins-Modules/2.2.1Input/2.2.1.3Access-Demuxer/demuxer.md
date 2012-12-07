acess Demux访问多路分配器

*  1:描述

access_demux模块的设计用来处理访问和同一模块中的解复用阶段的第一部分。        

因此，你需要读取访问和多路分配器页面，然后再前往。
 
可以被看作是一个demuxer处理在同一时间的接入访问和分路器。

在访问分路器，流s是空的。

访问分路器的例子是DVD，蓝光，V4L2模块

*  2：写访问的:多路分配器模块

要编写一个access_demuxer模块，开始阅读模块的写作。

然后，你应该指定你access_demux类型的模块

set_capability( "access_demux", 60 )

set_category( CAT_INPUT )

set_subcategory( SUBCAT_INPUT_ACCESS )

*  3：用函数来实现

实施Open（）和close（）函数，你将需要实现一些专业功能

正如你可以看到，在解复用，你应该定义：

解复用，在pf_demux

控制，pf_control NB

实现这些功能后，你应该将它们分配给相应的pf_功能。
   
*  4：多路分配器 

原型：

int (*pf_demux)  ( demux_t * );    

Return：   

当成功时候的一些积极的以及失败时候的一些消极的东西时，他应该返回0.

