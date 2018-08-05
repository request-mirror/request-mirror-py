import '../stylesheets/view'
import IO from 'socket.io-client'
import RequestList from './components/RequestList'
import React from 'react'
import ReactDOM from 'react-dom'

const socket = IO('http://localhost:5000');

class Requests extends React.Component {

    constructor(props) {
        super(props);
        this.state = {requests: []};
    }

    _receiveRequest(request) {
        const {requests} = this.state;
        requests.unshift(request);
        this.setState({requests});
    }

    componentDidMount() {
        socket.on('connect', () => socket.emit('join', code));
        socket.on('request', (request) => this._receiveRequest(request));
        socket.on('disconnect', () => socket.emit('leave', code));
    }

    render() {
        return (
            <RequestList requests={this.state.requests}/>
        )
    }
}

ReactDOM.render(
    <Requests/>,
    document.getElementById('request-list')
);