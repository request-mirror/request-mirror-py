import React from "react";
import Request from './Request'

const RequestList = ({requests}) => (
    <div className="requests">
        {requests.map((request, i) => {
            return (
                <Request
                    key={i}
                    method={request.method}
                    path={request.path}
                    time={request.time}
                    data={request.body}
                    queryParams={request.query_string}
                    formParams={request.form}
                    headers={request.headers}
                    host={request.remote_addr}
                />
            );
        })}
    </div>
);

export default RequestList;
