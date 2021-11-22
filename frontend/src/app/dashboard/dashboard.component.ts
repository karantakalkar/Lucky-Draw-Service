import { Component, OnInit, OnChanges, Input, Output, EventEmitter } from '@angular/core';
import { FormControl } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnChanges {

  @Input() user: any;
  @Input() data: any;

  tickets = new FormControl('1');
  luckydraw = new FormControl();
  regticket = new FormControl();
  winners: any;
  upcoming: any;

  ownedTickets: any;

  @Output() back = new EventEmitter();

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    console.log(this.data)
    this.luckydraw.valueChanges.subscribe((draw: any) => {
      this.getupcoming(draw);
    })
  }

  ngOnChanges(): void {
    this.winners = this.data.winners;
    this.luckydraw.setValue(this.data.draws[0]);
    this.ownedTickets = this.data.tickets.filter((ticket: any) => ticket.user == this.user.id );
  }

  order() {
    this.dataService.getRaffleTickets(this.tickets.value, { "user": this.user.id.toString() }).subscribe((res: any) => {
      this.ownedTickets = this.ownedTickets.concat(res);
    })
  }

  register() {
    this.dataService.registerInDraw(this.luckydraw.value.id, { "ticket_id": this.regticket.value }).subscribe((res: any) => {
       let index = this.ownedTickets.indexOf(this.regticket)
       this.ownedTickets.splice(index,1)
       this.ownedTickets.push(res.reg_ticket);
       this.regticket.setValue(null)
       console.log(res)
    }),
    (err: any) => {
      console.log(err.message)
      window.alert(err['message']);
    }
  }

  getupcoming(draw: any) {
    this.dataService.getUpcomingEvent(draw.id).subscribe((reward: any) => {
      this.upcoming = reward;
      this.upcoming['timing'] = draw.timing;
      console.log(this.upcoming)
    })
  }

  announce(reward: any) {
    this.dataService.computeWinner(this.luckydraw.value.id, { "redeem_date": reward.redeem_date }).subscribe((res: any) => {
      this.winners.push(res.winner)
      reward.is_won = true;
      this.getupcoming(this.luckydraw)
    })
  }

}
