import { Component, OnInit, Input } from '@angular/core';
import { News } from '../../classes/news';

@Component({
  selector: 'app-news-small',
  templateUrl: './news-small.component.html',
  styleUrls: ['./news-small.component.css']
})
export class NewsSmallComponent implements OnInit {

	@Input() news: News;
	
	constructor() {
	}

	ngOnInit(): void {
		console.log(this.news);
	}

}
