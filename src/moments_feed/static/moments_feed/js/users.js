const domContainer = document.querySelector('#popularUsers');
class PopularUsers extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        request('GET', '/rest-api/users/?format=json', {}, function (code, data) {
            if (code === 200) {
                let res = [];
                data = JSON.parse(data);
                if (data.results) {
                    data = data.results;
                }
                for (let user of data) {
                    let userSpan = React.createElement('a', {
                        key: user.username,
                        href: '/@' + user.username,
                        className: 'user'
                    }, user.username);
                    res.push(userSpan);
                }
                this.setState({ users: React.createElement('span', null, res) });
            }
        }.bind(this));
    }

    render() {
        if (this.state && this.state.users) {
            return this.state.users;
        } else {
            return 'Loading users...';
        }
    }
}
ReactDOM.render(React.createElement(PopularUsers), domContainer);
