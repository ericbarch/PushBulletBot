var PushBullet = require('pushbullet')
var pusher = new PushBullet('API_KEY')
var crypto = require('crypto')

var stream = pusher.stream()

stream.on('connect', function () {
  console.log('connect')
})
stream.on('close', function () {
  console.log('dc')
})
stream.on('error', function (error) {
  console.log(error)
})
stream.on('tickle', function (type) {
  if (type === 'push') {
    var options = {
      limit: 1
    }

    pusher.history(options, function (error, response) {
      if (!error && response.pushes.length === 1) {
        var pushText = response.pushes[0].body
        if (pushText && pushText.toLowerCase() === 'flip') {
          var buf = crypto.randomBytes(1)
          var byteDec = buf.readUInt8(0)
          var coinResult

          if (byteDec % 2 === 0) {
            coinResult = 'Heads'
          } else {
            coinResult = 'Tails'
          }

          pusher.note(response.pushes[0].source_device_iden, coinResult, '', function (error, response) {
            if (error) {
              console.log('error pushing coin flip')
            }
          })
        }
      }
    })
  }
})

var options = {
  limit: 10
}

pusher.devices(options, function (error, response) {
  if (error) {
    return console.log('could not query device list')
  }

  var foundMe = false

  for (var i = 0; i < response.devices.length; i++) {
    if (response.devices[i].active) {
      console.log(response.devices[i].nickname)

      if (response.devices[i].nickname === 'coinbot') {
        foundMe = true
      }
    }
  }

  if (!foundMe) {
    pusher.createDevice('coinbot', function (error, response) {
      if (!error) {
        stream.connect()
      } else {
        console.log(error)
      }
    })
  } else {
    stream.connect()
  }
})

