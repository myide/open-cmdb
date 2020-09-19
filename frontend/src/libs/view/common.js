
export const alertWarning = (action, notice, name_id) => {
  let action_map = {
    'create': '创建',
    'update': '更新',
    'delete': '删除',
    'fetchInfo': '采集信息',
    'sync': '同步信息'
  }
  let action_desc = action_map[action]
  notice.success({
    title: action_desc,
    duration: 6,
    render: h => {
      if (action === 'create') {
        var desc = h('p', {}, name_id + ' 已' + action_desc)
      } else {
        desc = h('p', {}, '资源（ID: ' + name_id + ' ）已' + action_desc)
      }
      let subTags = [desc]
      return h('div', subTags)
    }
  })
}
