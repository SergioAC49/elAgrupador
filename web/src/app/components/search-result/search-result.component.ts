import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { NewsService } from '../../services/news.service';
import { News } from '../../classes/news';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {

	public searchValue: string;
	public news$: Observable<any>;
	public news: News;

	constructor(public service: NewsService, private route: ActivatedRoute) {


		this.route.queryParams.subscribe(params => {
			this.searchValue = params['value'];
		});
		

	    this.service.search(this.searchValue).subscribe(data => {
	    	console.log(data);
	    	data.forEach( (element) => {
	    		element.id = element._id;
	    		element.newspaper = element._source.newspaper;
	    		element.title = element._source.title;
	    		element.picture_url = element._source.picture_url;
	    	});
	    	this.news = data;
	    });
	}

	ngOnInit(): void { }		

}
