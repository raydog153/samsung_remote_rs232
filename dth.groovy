/**
 *  Copyright 2015 SmartThings
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 *  Samsung TV RS232 Control
 *
 *  Author: SmartThings (juano23@gmail.com)
 *  Date: 2019-02-06
 */

def clientVersion() {
    return "00.00.01"
}

metadata {
	definition (name: "Samsung TV RS232", namespace: "smartthings", author: "Ray Boutotte", ocfDeviceType: "oic.d.switch", mnmn: "SmartThings", vid:"generic-switch") {
    	capability "Switch" 
		capability "Refresh"
		capability "Polling"
		capability "Health Check"
            
        command "mute" 
        command "source"
        command "menu"    
        command "tools"           
        command "tvsleep"
        command "up"
        command "down"
        command "left"
        command "right" 
        command "chup" 
        command "chdown"               
        command "prech"
        command "volup"    
        command "voldown"           
        command "enter"
        command "key_return"
        command "exit"
        command "info"            
        command "size"
	}

	tiles(scale: 1) {
		multiAttributeTile(name:"switch", type: "generic", width: 6, height: 4, canChangeIcon: true){
			tileAttribute ("device.switch", key: "PRIMARY_CONTROL") {
				attributeState "on", label: '${name}', action: "switch.off", icon: "st.switches.switch.on", backgroundColor: "#00a0dc"
				attributeState "off", label: '${name}', action: "switch.on", icon: "st.switches.switch.off", backgroundColor: "#ffffff"
			}
		}
        standardTile("refresh", "device.status", width: 2, height: 2, inactiveLabel: false, decoration: "flat") {
            state "default", action:"refresh.refresh", icon:"st.secondary.refresh", defaultState: true
        }
        standardTile("mute", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Mute', action:"mute", icon:"st.custom.sonos.muted", backgroundColor:"#ffffff"
        }    
        standardTile("source", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Source', action:"source", icon:"st.Electronics.electronics15"
        }
        standardTile("tools", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Tools', action:"tools", icon:"st.secondary.tools"
        }
        standardTile("menu", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Menu', action:"menu", icon:"st.vents.vent"
        }
        standardTile("tvsleep", "device.switch", width: 2, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Sleep', action:"tvsleep", icon:"st.Bedroom.bedroom10"
        }
        standardTile("up", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Up', action:"up", icon:"st.thermostat.thermostat-up"
        }
        standardTile("down", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Down', action:"down", icon:"st.thermostat.thermostat-down"
        }
        standardTile("left", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Left', action:"left", icon:"st.thermostat.thermostat-left"
        }
        standardTile("right", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Right', action:"right", icon:"st.thermostat.thermostat-right"
        }  
        standardTile("chup", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'CH Up', action:"chup", icon:"st.thermostat.thermostat-up"
        }
        standardTile("chdown", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'CH Down', action:"chdown", icon:"st.thermostat.thermostat-down"
        }
        standardTile("prech", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Pre CH', action:"prech", icon:"st.secondary.refresh-icon"
        }
        standardTile("volup", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Vol Up', action:"volup", icon:"st.thermostat.thermostat-up"
        }
        standardTile("voldown", "device.switch", width: 2, height: 2, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Vol Down', action:"voldown", icon:"st.thermostat.thermostat-down"
        }
        standardTile("enter", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Enter', action:"enter", icon:"st.illuminance.illuminance.dark"
        }
        standardTile("key_return", "device.switch", width: 2, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Return', action:"key_return", icon:"st.secondary.refresh-icon"
        }
        standardTile("exit", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Exit', action:"exit", icon:"st.locks.lock.unlocked"
        }    
        standardTile("info", "device.switch", width: 1, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Info', action:"info", icon:"st.motion.acceleration.active"
        }    
        standardTile("size", "device.switch", width: 2, height: 1, decoration: "flat", canChangeIcon: false) {
            state "default", label:'Picture Size', action:"size", icon:"st.contact.contact.open"
        }      
        standardTile("blank", "device.switch", width: 1, height: 1, canChangeIcon: false,  canChangeBackground: false, decoration: "flat") {
        	state "default", label: "", action: "", icon: "", backgroundColor: "#FFFFFF", defaultState: true
        }
        standardTile("blank2x", "device.switch", width: 2, height: 1, canChangeIcon: false,  canChangeBackground: false, decoration: "flat") {
        	state "default", label: "", action: "", icon: "", backgroundColor: "#FFFFFF", defaultState: true
        }
        // carouselTile("cameraDetails", "device.image", width: 4, height: 2) { }
        main "switch"
        details (["switch",
                  "volup","mute","chup",
                  "voldown","source","chdown",
                  "menu","up","tools","blank","size",
                  "left","enter","right","blank","tvsleep",
                  "info","down","exit","blank","key_return"
                 ])	
	}
}

def installed() {
	log.trace "method called: installed"
}
 
def updated() {
	log.trace "method called: updated"
 	unschedule()
 	runEvery5Minutes(refresh)
 	runIn(2, refresh)
}

def parse(String description) {
    // This will never be called for cloud devices, which are any networked device. 
	log.trace "method called: parse"
    log.debug description
	return null
}

def ping() {
	log.debug "Pinging device because it has not checked in..."
	refresh()
}
def poll() {
	log.trace "method called: poll"
	tvAction("POWER_STATUS", "c0a80164:D6D8")
}

def refresh() {
	log.trace "method called: refresh"
	tvAction("POWER_STATUS", "c0a80164:D6D8")
}

private tvAction(key,deviceNetworkId) {
    log.debug "Executing ${key}"
    
    // Standard Connection Data
    // TODO Handle com port setting if needed
    def remoteName = "SmartThings".encodeAsBase64().toString()
    def remoteNameLength = remoteName.getBytes().size()

    // Device Connection Data
    def ipAddress = convertHexToIP("c0a80164").encodeAsBase64().toString()
    def ipAddressHex = "c0a80164" // deviceNetworkId.substring(0,8)
    def ipAddressLength = ipAddress.getBytes().size()
    
    def macAddress = "0011328E4EE9".encodeAsBase64().toString()
    def macAddressLength = macAddress.getBytes().size()

    log.debug "ipAddress: ${ipAddress}"
    
    // Build the command we will send to the Samsung TV
    //def command = "KEY_${key}".encodeAsBase64().toString()

    // Send both the authentication and action at the same time
    def request = new physicalgraph.device.HubAction(
        method: "GET",
        path: "/" + "KEY_${key}",
        headers: [
                 "HOST" : "192.168.1.100:55000",
                 "Content-Type": "text/json"
                 ],
        null,
        [callback: calledBackHandler]
	)
    log.debug request.toString()
    sendHubCommand(request);
}

// the below calledBackHandler() is triggered when the device responds to the sendHubCommand() with "tvAction" resource
void calledBackHandler(physicalgraph.device.HubResponse hubResponse) {
    log.debug("Entered calledBackHandler() is: ${hubResponse}")
    //log.debug("body in calledBackHandler() is: ${hubResponse.body}")
    log.debug("body in calledBackHandler() is: ${hubResponse.json}")
    //log.debug("data in calledBackHandler() is: ${hubResponse.data}")
    
    state.lastUpdated = new Date().time
    log.trace "calling currentState"
    if (device.currentState("switch") == null) {
    	log.debug "currentState is null, so setting..."
    	sendEvent(name: "switch", value: "on", isStateChange: true, display: false)
    }
    log.trace "called currentState"
    def currstate = device.currentState("switch").getValue()
    def isStateChange = (state.power_status != hubResponse.json['power_status'])
    if ((currstate == "on" && state.power_status == false) || (currstate == "off" && state.power_status == true)) {
    	isStateChange = true
    }
    else {
    	log.trace "no state change??"
    }
    // log.debug currstate
    // log.debug isStateChange
    if (currstate == "on" && isStateChange) {
    	log.debug "setting currentState to off"
    	sendEvent(name: "switch", value: "off", isStateChange: true, display: false)
    }
    else if (currstate == "off" && isStateChange) {
    	log.debug "setting currentState to on"
        sendEvent(name: "switch", value: "on", isStateChange: true, display: false)
    }
    state.power_status = hubResponse.json['power_status']
}

def on() {
	log.debug "Turning TV ON"
    tvAction("POWERON",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Power On", displayed: true) 
}

def off() {
	log.debug "Turning TV OFF"
    tvAction("POWEROFF",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Power Off", displayed: true) 
}

def mute() {
	log.trace "MUTE pressed"
    tvAction("MUTE",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Mute", displayed: true) 
}

def source() {
	log.debug "SOURCE pressed"
    tvAction("SOURCE",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Source", displayed: true) 
}

def menu() {
	log.debug "MENU pressed"
    tvAction("MENU",device.deviceNetworkId) 
}

def tools() {
	log.debug "TOOLS pressed"
    tvAction("TOOLS",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Tools", displayed: true)     
}

def tvsleep() {
	log.debug "SLEEP pressed"
    tvAction("SLEEP",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Sleep", displayed: true)
}

def up() {
	log.debug "UP pressed"
    tvAction("UP",device.deviceNetworkId)
}

def down() {
	log.debug "DOWN pressed"
    tvAction("DOWN",device.deviceNetworkId) 
}

def left() {
	log.debug "LEFT pressed"
    tvAction("LEFT",device.deviceNetworkId) 
}

def right() {
	log.debug "RIGHT pressed"
    tvAction("RIGHT",device.deviceNetworkId) 
}

def chup() {
	log.debug "CHUP pressed"
    tvAction("CHUP",device.deviceNetworkId)
    sendEvent(name:"Command", value: "Channel Up", displayed: true)         
}

def chdown() {
	log.debug "CHDOWN pressed"
    tvAction("CHDOWN",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Channel Down", displayed: true)     
}

def prech() {
	log.debug "PRECH pressed"
    tvAction("PRECH",device.deviceNetworkId)
    sendEvent(name:"Command", value: "Prev Channel", displayed: true)       
}

def exit() {
	log.debug "EXIT pressed"
    tvAction("EXIT",device.deviceNetworkId) 
}

def volup() {
	log.debug "VOLUP pressed"
    tvAction("VOLUP",device.deviceNetworkId)
    sendEvent(name:"Command", value: "Volume Up", displayed: true)         
}

def voldown() {
	log.debug "VOLDOWN pressed"
    tvAction("VOLDOWN",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Volume Down", displayed: true)         
}

def enter() {
	log.debug "ENTER pressed"
    tvAction("ENTER",device.deviceNetworkId) 
}

def key_return() {
	log.debug "RETURN pressed"
    tvAction("RETURN",device.deviceNetworkId) 
}

def info() {
	log.debug "INFO pressed"
    tvAction("INFO",device.deviceNetworkId) 
	sendEvent(name:"Command", value: "Info", displayed: true)    
}

def size() {
	log.debug "PICTURE_SIZE pressed"
    tvAction("PICTURE_SIZE",device.deviceNetworkId) 
    sendEvent(name:"Command", value: "Picture Size", displayed: true)
}

private Integer convertHexToInt(hex) {
	Integer.parseInt(hex,16)
}

private String convertHexToIP(hex) {
	[convertHexToInt(hex[0..1]),convertHexToInt(hex[2..3]),convertHexToInt(hex[4..5]),convertHexToInt(hex[6..7])].join(".")
}
