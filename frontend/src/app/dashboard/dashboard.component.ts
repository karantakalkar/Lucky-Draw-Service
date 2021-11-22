import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  @Input() user: any;
  @Input() data: any;

  @Output() back = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
    console.log(this.data)
  }

}
