package main

import (
	"github.com/putsi/paparazzogo"
	"log"
	"net/http"
	"time"
)

func main() {
	// local server settings
	imgPath := "/img.jpg"
	addr := ":8080"

	// MJPEG-stream settings
	user := ""
	pass := ""

	// Stream times out after 30s
	timeout := 30 * time.Second
	mjpegStream := "http://balena-cam:5150/mjpeg"

	mjpegHandler := paparazzogo.NewMjpegproxy()
	mjpegHandler.OpenStream(mjpegStream, user, pass, timeout)

	http.Handle(imgPath, mjpegHandler)

	s := &http.Server{
		Addr:		addr,
		Handler:	mux,
		// Read & Write timeout prevent server from getting overwhelmed with idle connections
		ReadTimeout:	10 * time.Second
		WriteTimeout:	10 * time.Second
	}

	log.Fatal(s.ListenAndServe())

	// IDK WHAT THIS DOES ~ CHRISTIAN ~
	block := make(chan bool)
	// time.Sleep(time.Second * 30)
	// mp.CloseStream()
	// mp.OpenStream(newMjpegstream, newUser, newPass, newTimeout)
	<-block
}