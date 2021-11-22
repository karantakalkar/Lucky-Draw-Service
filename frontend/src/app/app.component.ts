import { Component } from '@angular/core';
import { DataService } from './data.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  user: any;
  data: any = {};

  toggle: boolean = false;

  constructor(private dataService: DataService) {

    this.dataService.getLuckyDraws().subscribe((draws: any) => { this.data['draws'] = draws })
    this.dataService.getTicketsList().subscribe((tickets: any) => { this.data['tickets'] = tickets })
    this.dataService.getWinners(7).subscribe((winners: any) => { this.data['winners'] = winners})

  }

  showDash($event: any) {
    this.toggle = true;
    this.user = $event;
  }

}
