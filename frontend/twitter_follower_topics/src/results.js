class resultsPage extends Component {

  constructor(props){
    super(props);
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input type="text" value={this.state.search} className="searchbar" placeholder="Search" onChange={this.handleChange} />
        <input type="submit" value="Submit" />
      </form>
      );
  }
}