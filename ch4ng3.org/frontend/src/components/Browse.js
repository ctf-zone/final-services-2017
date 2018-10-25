import React, { Component } from 'react'
import PetitionsList from './PetitionsList'

class Browse extends Component {

  render() {

    return (
      <PetitionsList
        emptyMessage='There are no petitions :('
        filter={{}} />
    )
  }
}

export default Browse
