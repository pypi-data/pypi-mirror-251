export const id=981;export const ids=[981];export const modules={981:(t,e,i)=>{i.r(e),i.d(e,{LCNEntitiesPage:()=>f});var s=i(309),a=i(4541),n=i(7838),d=i(8144),o=i(4243),r=(i(657),i(1952),i(4776),i(8336),i(7662),i(9040),i(4371),i(4516)),l=i(1750),c=i(9051);(0,s.Z)([(0,o.Mo)("lcn-entities-data-table")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"device",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"entities",value(){return[]}},{kind:"field",key:"_entities",value(){return(0,r.Z)((t=>t.map((t=>({...t,delete:t})))))}},{kind:"field",key:"_columns",value(){return(0,r.Z)((t=>t?{name:{title:this.lcn.localize("name"),sortable:!0,direction:"asc",grows:!0}}:{name:{title:this.lcn.localize("name"),sortable:!0,direction:"asc",grows:!0,width:"35%"},domain:{title:this.lcn.localize("domain"),sortable:!0,grows:!1,width:"25%"},resource:{title:this.lcn.localize("resource"),sortable:!0,grows:!1,width:"25%"},delete:{title:"",sortable:!1,width:"80px",template:t=>d.dy`
                  <ha-icon-button
                    title=${this.lcn.localize("dashboard-entities-table-delete")}
                    .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                    @click=${e=>this._onEntityDelete(e,t)}
                  ></ha-icon-button>
                `}}))}},{kind:"method",key:"render",value:function(){return d.dy`
      <ha-data-table
        .hass=${this.hass}
        .columns=${this._columns(this.narrow)}
        .data=${this._entities(this.entities)}
        .id=${"unique_id"}
        .noDataText=${this.lcn.localize("dashboard-entities-table-no-data")}
        .dir=${(0,l.Zu)(this.hass)}
        auto-height
        clickable
      ></ha-data-table>
    `}},{kind:"method",key:"_onEntityDelete",value:function(t,e){t.stopPropagation(),this._deleteEntity(e.address,e.domain,e.resource)}},{kind:"method",key:"_deleteEntity",value:async function(t,e,i){const s=this.entities.find((s=>s.address[0]===t[0]&&s.address[1]===t[1]&&s.address[2]===t[2]&&s.domain===e&&s.resource===i));await(0,c.Ks)(this.hass,this.lcn.host.id,s),this.dispatchEvent(new CustomEvent("lcn-configuration-changed",{bubbles:!0,composed:!0}))}}]}}),d.oi);var h=i(8394);const u=()=>Promise.all([i.e(597),i.e(321),i.e(812),i.e(719),i.e(527)]).then(i.bind(i,6527));let f=(0,s.Z)([(0,o.Mo)("lcn-entities-page")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Array,reflect:!1})],key:"tabs",value(){return[]}},{kind:"field",decorators:[(0,o.SB)()],key:"_deviceConfig",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_entityConfigs",value(){return[]}},{kind:"method",key:"firstUpdated",value:async function(t){(0,a.Z)((0,n.Z)(i.prototype),"firstUpdated",this).call(this,t),u(),await this._fetchEntities(this.lcn.host.id,this.lcn.address)}},{kind:"method",key:"render",value:function(){return this._deviceConfig||0!==this._entityConfigs.length?d.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/lcn/devices"
        .tabs=${this.tabs}
      >
        <ha-config-section .narrow=${this.narrow}>
          <span slot="header"> ${this.lcn.localize("dashboard-entities-title")} </span>

          <span slot="introduction"> ${this.lcn.localize("dashboard-entities-introduction")} </span>

          <ha-card
            header="Entities for ${this._deviceConfig.address[2]?this.lcn.localize("group"):this.lcn.localize("module")}
              (${this.lcn.host.name}, ${this._deviceConfig.address[0]},
              ${this._deviceConfig.address[1]})
              ${this._deviceConfig.name?" - "+this._deviceConfig.name:""}
            "
          >
            <lcn-entities-data-table
              .hass=${this.hass}
              .lcn=${this.lcn}
              .entities=${this._entityConfigs}
              .device=${this._deviceConfig}
              .narrow=${this.narrow}
              @lcn-configuration-changed=${this._configurationChanged}
            ></lcn-entities-data-table>
          </ha-card>
        </ha-config-section>
        <ha-fab
          slot="fab"
          @click=${this._addEntity}
          .label=${this.lcn.localize("dashboard-entities-add")}
          extended
        >
          <ha-svg-icon slot="icon" path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `:d.dy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"_configurationChanged",value:function(){this._fetchEntities(this.lcn.host.id,this.lcn.address)}},{kind:"method",key:"_fetchEntities",value:async function(t,e){const i=(await(0,c.LO)(this.hass,t)).find((t=>t.address[0]===e[0]&&t.address[1]===e[1]&&t.address[2]===e[2]));void 0!==i&&(this._deviceConfig=i),this._entityConfigs=await(0,c.rI)(this.hass,t,e)}},{kind:"method",key:"_addEntity",value:async function(){var t,e;t=this,e={lcn:this.lcn,device:this._deviceConfig,createEntity:async t=>!!(await(0,c.Ce)(this.hass,this.lcn.host.id,t))&&(await this._fetchEntities(this.lcn.host.id,this.lcn.address),!0)},(0,h.B)(t,"show-dialog",{dialogTag:"lcn-create-entity-dialog",dialogImport:u,dialogParams:e})}}]}}),d.oi)}};
//# sourceMappingURL=UIZd3ocm.js.map