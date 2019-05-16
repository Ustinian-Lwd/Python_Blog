
	function show_date_time() {
		// 隔一秒运行当前程序
		window.setTimeout("show_date_time()", 1000);
		// 网站写成之日
		BirthDay = new Date("04/13/2019 0:0:0");
		// 当前时间
		today = new Date();
		// 时间差
		timeold = (today.getTime() - BirthDay.getTime());
		// 秒
		sectimeold = timeold / 1000
		// 
		secondsold = Math.floor(sectimeold);
		msPerDay = 24 * 60 * 60 * 1000
		e_daysold = timeold / msPerDay
		daysold = Math.floor(e_daysold);
		e_hrsold = (e_daysold - daysold) * 24;
		hrsold = Math.floor(e_hrsold);
		e_minsold = (e_hrsold - hrsold) * 60;
		minsold = Math.floor((e_hrsold - hrsold) * 60);
		seconds = Math.floor((e_minsold - minsold) * 60);
		var span_dt_dt = document.getElementById("span_dt_dt")
		span_dt_dt.innerHTML = '<font style=color:#C40000>' + daysold + '</font> 天 <font style=color:#C40000>' + hrsold + '</font> 时 <font style=color:#C40000>' + minsold + '</font> 分 <font style=color:#C40000>' + seconds + '</font> 秒';
}

show_date_time(); 

var _hmt = _hmt || [];
(function() {
	var hm = document.createElement("script");
	hm.src = "https://hm.baidu.com/hm.js?f643ef522aa682d0bae0feaa53dfbce3";
	var s = document.getElementsByTagName("script")[0];
	s.parentNode.insertBefore(hm, s);
});
	
