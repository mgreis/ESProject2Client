// tutorial21.js
var JobBox = React.createClass({
  loadJobsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleJobSubmit: function(job) {
    var jobs = this.state.data;
    job.id = Date.now();
    var newJobs = jobs.concat([job]);
    this.setState({data: newJobs});
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: job,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        this.setState({data: jobs});
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadJobsFromServer();
    setInterval(this.loadJobsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="jobBox">
        <h1>Jobs</h1>
        <JobForm onJobSubmit={this.handleJobSubmit} />
        <JobList data={this.state.data} />

      </div>
    );
  }
});

var JobList = React.createClass({
  render: function() {
    var jobNodes = this.props.data.map(function(job) {
      return (
        <Job  key           = {job.job_id}
              job_id        = {job.job_id}
              job_state     = {job.job_state}
              job_submitted = {job.job_submitted}
              job_started   = {job.job_started}
              job_finished  = {job.job_finished}
              job_file      = {job.job_file}
        >
        </Job>
      );
    });
    return (
      <div className="JobList">
          {jobNodes}
      </div>
    );
  }
});

var Job = React.createClass({


  render: function() {
    return (
      <div className="job">
          <br/>
            <p className="jobAuthor">
                id:           {this.props.job_id}<br/>
                State:        {this.props.job_state}<br/>
                Submitted on: {this.props.job_submitted}<br/>
                Started on:   {this.props.job_started}<br/>
                Finished on:  {this.props.job_finished}<br/>
                File name:    {this.props.job_file}<br/><br/>
            </p>
      </div>
    );
  }
});

var JobForm = React.createClass({
  getInitialState: function() {
    return {author: '', text: ''};
  },
  handleAuthorChange: function(e) {
    this.setState({author: e.target.value});
  },
  handleTextChange: function(e) {
    this.setState({text: e.target.value});
  },
  handleSubmit: function(e) {
    e.preventDefault();
    var author = this.state.author.trim();
    var text = this.state.text.trim();
    if (!text || !author) {
      return;
    }
    this.props.onJobSubmit({author: author, text: text});
    this.setState({author: '', text: ''});
  },
  render: function() {
    return (
      <form className="jobForm" onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Your name"
          value={this.state.author}
          onChange={this.handleAuthorChange}
        /><br/>
        <input
          type="text"
          placeholder="Say something..."
          value={this.state.text}
          onChange={this.handleTextChange}
        /><br/>
        <input type="submit" value="Post" />
      </form>
    );
  }
});






ReactDOM.render(
    <JobBox url="/manage_jobs_react"
            pollInterval = {10000}
            />,

    document.getElementById('content')
);
