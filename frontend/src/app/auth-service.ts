import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../environments/environment'

const API_URL = environment.apiUrl;

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  /**
   * @param {HttpClient} http Http Client to send requests.
   */
  constructor(private http: HttpClient) { }

  login(data: { username: string, password: string }): Observable<any> {
    return this.http.post(API_URL + '/users/login/', data);
  }

  signup(data: { username: string, password: string }): Observable<any> {
    return this.http.post(API_URL + '/users/', data);
  }

}
