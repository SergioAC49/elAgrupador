import { Component, OnInit } from '@angular/core';

import { NewsService } from '../../services/news.service';
import { News } from '../../classes/news';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent implements OnInit {

	public news: News;

	constructor(public service: NewsService) {

	    this.service.getNews().subscribe(data => {
	    	this.news = data[0];
	    	console.log(this.news);
	    });
	}

	ngOnInit(): void {}

}
