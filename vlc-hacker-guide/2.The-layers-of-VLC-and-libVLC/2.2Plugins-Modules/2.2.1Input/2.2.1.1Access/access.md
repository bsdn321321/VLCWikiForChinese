nput/access
>1:描述 
>>'access'的模块被设计成一个模块链的第一个和最后一个元素。访问输入和输出处理大部分的基本I / O的VLC。它们通常是协议实现（HTTP，FTP等）或设备的访问。     
>> 在此页面中我们将讨论输入访问
>
>2：写访问模块  
>>写一个访问模块，你应该编写访问模块，阅读模块介绍，你应该指定模块的访问类型。   
>>set_capability( "access", 60 )     
>>set_category( CAT_INPUT)   
>>set_subcategory( SUBCAT_INPUT_ACCESS )   
>你的模块可以是一个'块'或'阅读'类型，根据您的媒体选择：  
 >> 如果底层协议返回未知大小的数据块，块是一个更好的类型，   
 >> 如果你控制的底层协议所要求的数据的大小，阅读是一个更好的类型。
>                                     
>3：运用函数来实现某些功能   
>>实施后，Open（）和close（）函数，你将需要实现一些专业功能，将您的功能实现。
你可以看到include/vlc_access.h§,，如下定义：   
>>Seek 在pf_seek  
>>Control在pf_control   
>>Read or block这取决于你的模块类型   
>4：seek  
>>原型: 
>>int         (*pf_seek) ( access_t *, uint64_t );
>>当有请求时，函数将会被调用。  
>>该参数是一个指针的模块结构，指明所要求的位置。    
 注：如果没有可能寻求协议或设备，seek函数可以为NULL。    
>>您应设置p_access的 - > info.b_eof为false，如果seek 工作。   
>>return：   
>>如果seek成功，它应该返回VLC_SUCCESS的，否则它应该返回VLC_EGENERIC。  
>5：control  
>>原型:
>>int         (*pf_control)( access_t *, int i_query, va_list args);  
>>控制功能是很容易的，输入核心模块将查询使用此功能：       
  >>模块结构的指针。  
  >>一个i_query参数，可以是几种类型。之后我们将介绍最重要的。   
 >> 参数列表，这取决于的i_query类型。  
>>Return:  
>>如果查询成功，它应该返回VLC_SUCCESS。否则它，应该返回VLC_EGENERIC.   
>5.1 控制查询类型  
>>首当其冲的是知道什么该模块支持的要求。它们都是布尔类型的，应该总是成功
>>>ACCESS_CAN_SEEK,        
>>>ACCESS_CAN_FASTSEEK,    
>>>ACCESS_CAN_PAUSE,       
>>>ACCESS_CAN_CONTROL_PACE,
>>下面的一个是一个请求的PTS延迟 
ACCESS_GET_PTS_DELAY,   
>  
>>以下是要求对输入的各种信息，如元数据，标题和章节或设备的信号强度。所有这些可能会失败。    
>>>ACCESS_GET_TITLE_INFO,  
>>>ACCESS_GET_META,        
>>>ACCESS_GET_CONTENT_TYPE,
>>>ACCESS_GET_SIGNAL,    
>  
>>根据CAN_要求，可以设置几件事情，如暂停或改变标题或章节.
>>>ACCESS_SET_PAUSE_STATE,
>>>ACCESS_SET_TITLE,
>>>ACCESS_SET_SEEKPOINT      
>>你可以找到对应的的access_query_e定义vlc_access.h的查询类型的参数列表  
>
>6：read   
>>原型：       
ssize_t     (*pf_read) ( access_t *, uint8_t *, size_t );    
Return   
>>如果没有数据返回-1，否则读取其他数据。
>  
>7: block  
>>原型：      
block_t    *(*pf_block)( access_t * );      
Return       


B
B
B
B
A
A
B
B
B
B
A
A
B
B
以‘natural’大小返回数据块，如果还没有数据或者eof它会返回null.为了区分数据和EOF之间没有，你应当设置为true的情况下，EOF p_access - > info.b_eof。
