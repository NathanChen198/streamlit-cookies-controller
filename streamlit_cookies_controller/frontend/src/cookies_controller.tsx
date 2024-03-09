/*
author: Nathan Chen
date  : 08-Mar-2024
*/


import {
  Streamlit,
  withStreamlitConnection,
  StreamlitComponentBase,
} from "streamlit-component-lib"
import React, {
  ComponentProps
} from "react"
import Cookies from "universal-cookie"


enum Method{
  getAll = 'getAll',
  get = 'get',
  set = 'set',
  remove = 'remove'
}


interface State{
  prv_cookies: any
}


const cookies = new Cookies();


const set = (name: string, value: any, options: any) =>{
  const converted_options = { expires: new Date(options.expires) }
  options = { ...options, ...converted_options }
  cookies.set(name, value, options)
}



class CookieController extends StreamlitComponentBase<State>{
  constructor(props: ComponentProps<any>){
    super(props);
    this.state = {
      prv_cookies: null
    }
  }

  componentDidMount(): void {
    super.componentDidMount();
    Streamlit.setFrameHeight(0);
  }

  componentDidUpdate(): void {
    super.componentDidUpdate();
    Streamlit.setFrameHeight(0);
  }

  render(): React.ReactNode {
    const args = this.props.args
    const method: Method = args['method']
    const name: string = args['name']
    let output = null;
    switch(method){
      case Method.getAll:
        output = cookies.getAll()
        break;
      case Method.get:
        output = cookies.get(name)
        break;
      case Method.set:
        set(name, args['value'], args['options'])
        break;
      case Method.remove:
        cookies.remove(name, args['options'])
        break;
      default:
        console.error(method + " is not recognized")
        break;
    }

    if(output && JSON.stringify(this.state.prv_cookies) !== JSON.stringify(output)){
      this.setState({
        prv_cookies: output
      })
      Streamlit.setComponentValue(output);
      Streamlit.setComponentReady();
    }

    return (<div />)
  }
}


export default withStreamlitConnection(CookieController)
