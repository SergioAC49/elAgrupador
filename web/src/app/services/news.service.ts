import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable,of, from } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { News } from '../classes/news';
import { Article } from '../classes/article';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

	private baseUrl: "http://cluster-rdlab.cs.upc.edu:50416/news/";

	constructor(public httpClient: HttpClient) { }

	getNews(): Observable<News[]> {
		return this.httpClient.get<News[]>("http://cluster-rdlab.cs.upc.edu:50416/news/latest")
		    .pipe(
		    	tap(_ => this.log('fetched news')),
		    	catchError(this.handleError<News[]>('getNews', []))
		    );
	}

	getArticle(id: string): Observable<Article> {
		const url = "http://cluster-rdlab.cs.upc.edu:50416/news/".concat(id.toString()).concat("/similar/");
		console.log("URL: ", url);
		return this.httpClient.get<Article>(url)
			.pipe(
				tap(_ => this.log(`fetched article id=${id}`)),
				catchError(this.handleError<Article>(`getArticle id=${id}`))
			);
	}

/*	search(words: string): Observable<Article[]> {
		const url = "http://cluster-rdlab.cs.upc.edu:50416/search/";
		console.log("URL: ", url);

	    let formData: FormData = new FormData(); 
	    formData.append('words', words);
	    return this.httpClient.post(url, formData)
			.pipe(
				tap(_ => this.log(`fetched article id=${id}`)),
				catchError(this.handleError<Article>(`getArticle id=${id}`))
			);
	}*/

	/**
	 * Handle Http operation that failed.
	 * Let the app continue.
	 * @param operation - name of the operation that failed
	 * @param result - optional value to return as the observable result
	 */
	private handleError<T>(operation = 'operation', result?: T) {
		return (error: any): Observable<T> => {

			// TODO: send the error to remote logging infrastructure
			console.error(error); // log to console instead

			// TODO: better job of transforming error for user consumption
			this.log(`${operation} failed: ${error.message}`);

			// Let the app keep running by returning an empty result.
			return of(result as T);
		};
	}

	private log(message: string) {
		console.log(`NewsService: ${message}`);
	}


}



