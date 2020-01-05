FROM solr:7.7

COPY --chown=solr solrcore/promising-practices /opt/solr/server/solr/mycores/promising-practices
COPY --chown=solr opioid-research /opt/solr/server/solr-webapp/webapp/opioid-research

EXPOSE 8983

