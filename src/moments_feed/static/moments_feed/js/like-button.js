document.querySelectorAll('.likeButton')
    .forEach(domContainer => {
        class LikeButton extends React.Component {
            constructor(props) {
                super(props);
                this.state = {
                    liked: this.props.liked
                };
            }

            sendRequest() {
                request('POST', this.props.requestUrl, {
                    like_moment: 'submit',
                    csrfmiddlewaretoken: this.props.csrfToken
                }, (code, data) => {
                    if (code === 200) {
                        data = JSON.parse(data);
                        let likesAmount = document.getElementById('likesAmount' + this.props.momentPk);
                        likesAmount.innerHTML = data.likesAmount;
                        this.setState({
                            liked: !this.state.liked
                        });
                    } else {
                        alert('Error ' + code);
                    }
                });
            }

            render() {
                let svgIcon = '#heart';
                let cls = 'hover-highlight';

                if (this.state.liked) {
                    svgIcon = '#heart-fill';
                    cls += ' liked';
                }

                return React.createElement(
                    'svg', {
                        width: '32',
                        height: '32',
                        className: cls,
                        onClick: () => {
                            this.sendRequest();
                        }
                    },
                    React.createElement(
                        'use', {
                            href: this.props.svgIconsUrl + svgIcon
                        },
                        ''
                    )
                );
            }
        }

        ReactDOM.render(React.createElement(
            LikeButton, {
                liked: !!parseInt(domContainer.dataset.liked, 10),
                momentPk: parseInt(domContainer.dataset.momentpk, 10),
                requestUrl: domContainer.dataset.requesturl,
                csrfToken: domContainer.dataset.csrftoken,
                svgIconsUrl: domContainer.dataset.svgiconsurl
            }),
            domContainer);
});