媒体播放器有一个强大的“对象变量”的infrastructure，可用于模块之间的信息传递。它可以比作一个观察者模式.

变量函数

var_Get 

va_Get* 功能将得到的值，如果这个变量存在（否则会出错）。

      var_Get ( vlc_object_t *, const char *, vlc_value_t * );
      var_GetBool( p_obj, psz_name );
      var_GetInteger( p_obj, psz_name );
      var_GetTime( p_obj, psz_name );
      var_GetFloat( p_obj, psz_name );
      var_GetString( p_obj, psz_name );
      var_GetNonEmptyString( p_obj, psz_name );
      var_GetAddress( p_obj, psz_name );

var_Inherit 

var_Inherit功能将得到默认值（从配置，例如）或被其parent对象设置的一组。

      var_Inherit
      var_InheritBool
      var_InheritInteger
      var_InheritFloat
      var_InheritString
      var_InheritTime
      var_InheritAddress
      var_InheritURational

var_CreateGet 

var_CreateGet*函数将创建变量的默认值，如果该变量尚未建立。如果该变量存在，在调用之前，它会得到的当前值（和增加其引用计数）。

      var_Create(a,b,c)
      var_CreateGetInteger(a,b)
      var_CreateGetBool(a,b)
      var_CreateGetTime(a,b)
      var_CreateGetFloat(a,b)
      var_CreateGetString(a,b)
      var_CreateGetNonEmptyString(a,b)
      var_CreateGetAddress(a,b)
      var_CreateGetIntegerCommand(a,b)
      var_CreateGetBoolCommand(a,b)
      var_CreateGetTimeCommand(a,b)
      var_CreateGetFloatCommand(a,b)
      var_CreateGetStringCommand(a,b)
      var_CreateGetNonEmptyStringCommand(a,b)

一个变量必须被创建，如果你想添加一个回调或改变一个变量的值（与var_Set）




