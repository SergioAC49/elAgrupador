import { Component, OnInit, Input } from '@angular/core';
import { News } from '../../classes/news';

@Component({
  selector: 'app-news-medium',
  templateUrl: './news-medium.component.html',
  styleUrls: ['./news-medium.component.css']
})
export class NewsMediumComponent implements OnInit {

	@Input() news: News;
	
	constructor() {
	}

	ngOnInit(): void {
		console.log(this.news);
	}

}
