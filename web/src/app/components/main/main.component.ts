import { Component, OnInit } from '@angular/core';

import { NewsService } from '../../services/news.service';
import { News } from '../../classes/news';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

	public news: News[];

	constructor(public service: NewsService) {

	    this.service.getNews().subscribe(data => {
	    	console.log(data);
	    	this.news = data;
	    });
	}

	ngOnInit(): void {}

}
