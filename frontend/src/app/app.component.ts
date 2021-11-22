import { Component, OnInit } from '@angular/core';
import { ElementRef, Renderer2 } from '@angular/core';
import { DataService } from './data.service';


// @ts-ignore
const confetti = require('canvas-confetti');

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  
  user: any;
  data: any = {};

  toggle: boolean = false;

  constructor(private dataService: DataService, 
              private renderer2: Renderer2,
              private elementRef: ElementRef) {

    this.dataService.getLuckyDraws().subscribe((draws: any) => { this.data['draws'] = draws })
    this.dataService.getTicketsList().subscribe((tickets: any) => { this.data['tickets'] = tickets })
    this.dataService.getWinners(7).subscribe((winners: any) => { this.data['winners'] = winners})

  }

  ngOnInit() {
    this.surprise();
  }

  public surprise(): void {
 
    const canvas = this.renderer2.createElement('canvas');
 
    this.renderer2.appendChild(this.elementRef.nativeElement, canvas);
 
    const myConfetti = confetti.create(canvas, {
      resize: true,
      particleCount: 100,
      spread: 100,
      origin: {
        y: 0.3
    }
    });
 
    myConfetti();
 
  }

  showDash($event: any) {
    this.toggle = true;
    this.user = $event;
  }


}
