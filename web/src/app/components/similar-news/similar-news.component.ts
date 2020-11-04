import { Component, OnInit, Input } from '@angular/core';

import { Article } from '../../classes/article';

@Component({
  selector: 'app-similar-news',
  templateUrl: './similar-news.component.html',
  styleUrls: ['./similar-news.component.css']
})
export class SimilarNewsComponent implements OnInit {

	@Input() articles: Article[];

	constructor() {}

	ngOnInit(): void {}

}
