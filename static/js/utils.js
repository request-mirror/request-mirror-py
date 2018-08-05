export function isEmpty(obj) {
    return obj === undefined ||
        (obj.constructor === String && obj === "") ||
        (obj.constructor === Object && Object.keys(obj).length === 0);
}
