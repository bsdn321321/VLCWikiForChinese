bility( "demux", 60 )

*  set_category( CAT_INPUT )

*  set_subcategory( SUBCAT_INPUT_DEMUX )

##用来实现的函数

在熟悉Open（）和close（）函数，你将需要实现一些majors features，将您的功能实现。正如你可以看到/ vlc_demux.h，你应该定义：

    Demux, as in pf_demux
    Control, as in pf_control 

##Demux

原型：

    int (*pf_demux)  ( demux_t * ); 

解复用功能是很容易的，从s*指针中提取数据的stream_t。
返回：

它应该返回0，EOF，有时候一些successful或者negtive的东西无法解复用。

##控制

原型：

    int         (*pf_control)( access_t *, int i_query, va_list args);

控制功能是很容易的，输入核心模块将查询使用此功能：

*模块结构的指针。

*它的一个i_query参数，可以是几种类型。之后我们将介绍最重要的。

*参数列表取决于的i_query类型。

返回：

如果查询成功，它应该返回VLC_SUCCESS。否则它，应该返回VLC_EGENERIC（失败）。

##Useful primitives

在实现解复用，你需要工作流，但同样也需要创造和控制轨道（ES）.

###Tracks / ES manipulation 

VLC的曲目被命名为ES基本流，你或许会需要：

*  es_out_Add
*  es_out_Send
*  es_out_Control 

###数据流的操作

数据流的操作可以完成的一些功能：

*  stream_Read
*   stream_Peek
*  stream_Control
*  stream_ReadLine
*  stream_Block 




 
 


