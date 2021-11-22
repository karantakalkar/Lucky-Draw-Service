import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormControl } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  @Input() user: any;
  @Input() data: any;

  tickets = new FormControl('1');

  @Output() back = new EventEmitter();

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    console.log(this.data)
  }

  order() {
    this.dataService.getRaffleTickets(this.tickets.value || 1, { "user": this.user.id.toString() }).subscribe((res: any) => {
      console.log(res);
    })
  }

}
