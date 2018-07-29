import React from 'react'
import {Card, CardBody, CardText, CardTitle} from 'reactstrap'
import log from '../log'

class Request extends React.Component {
    _title() {
        return (
            <CardTitle tag="h3">
                <strong>{this.props.method}</strong> {this.props.path}
                <small
                    className="text-muted">{this.props.time}</small>
            </CardTitle>
        )
    }

    render() {
        return (
            <Card>
                <CardBody>
                    {this._title()}
                    <ul>
                        {Object.keys(this.props.headers).map((header, i) => {
                            return (
                                <li key={i}>
                                    <strong>{header}: </strong>{this.props.headers[header]}
                                </li>
                            )
                        })}
                    </ul>
                    <p><samp>{this.props.data}</samp></p>
                    <samp>{this.props.queryString}</samp>
                </CardBody>
            </Card>
        )
    }
}

export default class RequestList extends React.Component {
    render() {
        log("RequestList requests:", this.props.requests);
        return (
            <div className="requests">
                {
                    this.props.requests.map((request, i) => {
                        return (
                            <Request
                                key={i}
                                method={request.method}
                                path={request.path}
                                time={request.time}
                                data={request.body}
                                queryString={request.query_string}
                                headers={request.headers}
                            />
                        )
                    })
                }
            </div>

        )
    }
}