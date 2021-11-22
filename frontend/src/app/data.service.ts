import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../environments/environment'

const API_URL = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class DataService {


  /**
   * @param {HttpClient} http Http Client to send requests.
   */
  constructor(private http: HttpClient) { }

  getTicketsList() {
    return this.http.get(API_URL + '/tickets');
  }

  getRaffleTickets(amount: any, data: any) {
    const httpParams = new HttpParams().set('amount', amount );
    return this.http.post(API_URL + '/tickets/', data, { params: httpParams });
  }

  getLuckyDraws(): Observable<any> {
    return this.http.get(API_URL + '/luckydraws');
  }

  registerInDraw(drawId: any, data: any) {
    return this.http.post(`${API_URL}/luckydraws/${drawId}/register`, data);
  }

  getUpcomingEvent(drawId: any) {
    return this.http.get(`${API_URL}/luckydraws/${drawId}/nextevent`);
  }

  computeWinner(drawId: any, data: any) {
    return this.http.post(`${API_URL}/luckydraws/${drawId}/compute`, data);
  }

  getWinners(span: any) {
    const httpParams = new HttpParams().set('span', span );
    return this.http.get(API_URL + '/winners/', { params: httpParams });
  }

}
