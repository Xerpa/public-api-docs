#!/usr/bin/env python3

import os
import json
import requests

def read_api_token():
    return(os.environ["lukla_api_token"])

def introspect(endpoint):
    headers = {
        "authorization": "Bearer " + read_api_token(),
        "content-type": "application/graphql"
    }
    u = endpoint + "/api/g"
    r = requests.post(u, data=query(), headers=headers)
    return(r.json())

def query():
    return("""
query {
  __schema {
    query_type { name }
    types {
      ...FullType
    }
    directives {
      name
      description
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: false) {
    name
    description
    type {
      ...TypeRef
    }
  }
  input_fields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enum_values(includeDeprecated: false) {
    name
    description
  }
  possible_types {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  of_type {
    kind
    name
    of_type {
      kind
      name
      of_type {
        kind
        name
        of_type {
          kind
          name
          of_type {
            kind
            name
            of_type {
              kind
              name
              of_type {
                kind
                name
                of_type {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}

    """)

def is_object(t):
    return(t["kind"] == "OBJECT")

def is_meta(t):
    return(t["name"].startswith("__"))

def camel_case_to_snake_case(t):
    if t.isupper():
        return("_{}".format(t.lower()))
    else:
        return(t)

def snake_case(text):
    return("".join([camel_case_to_snake_case(t) for t in text]))

def of_type(type_):
    kind = type_["kind"]
    if kind in ("NON_NULL", "LIST"):
        return(of_type(type_["of_type"]))
    elif kind in ("INTERFACE", "UNION"):
        return(("object", None))
    elif kind == "OBJECT":
        return((type_["name"], None))
    elif kind == "ENUM":
        return(("string", None))
    elif kind == "SCALAR":
        data_type = type_["name"].lower()
        if data_type in ("boolean", "string"):
            return((data_type, None))
        elif data_type in ("int", "float"):
            return(("number", None))
        else:
            return(("string", data_type))
    else:
        raise(RuntimeError)

def is_union(type_):
    kind = type_["kind"]
    subtype = type_["of_type"]
    if subtype:
        return(kind == "UNION" or is_union(subtype))
    else:
        return(kind == "UNION")

def map_field(field):
    return((snake_case(field["name"]), of_type(field["type"])))

def map_data_struct(type_, level):
    return((type_["name"], dict([map_field(f) for f in type_["fields"]])))

def map_schema(schema):
    types = schema["data"]["__schema"]["types"]
    data = dict([map_data_struct(t, 0) for t in types if is_object(t) and not is_meta(t)])
    return(data)

def allscalar(keys, known):
    scalars = ("number", "string", "object", "boolean")
    return(all(map(lambda x: x in known or x in scalars, keys)))

def format_field(field, type_0, cycles):
    if field[1][1]:
        return("+ {} ({}) -- {}".format(field[0], field[1][0], field[1][1]))
    else:
        type_1 = field[1][0]
        if (type_0, type_1) in cycles and type_1 in ("Profile", "Company"):
            return("+ {} (object) -- {}".format(field[0], type_1))
        else:
            return("+ {} ({})".format(field[0], type_1))

def format_type(type_, cycles):
    fields = "\n".join([format_field(field, type_[0], cycles) for field in type_[1].items()])
    return("\n## {} (object)\n\n{}\n".format(type_[0], fields))

def format_schema(schema, cycles):
    return("\n".join([format_type(type_, cycles) for type_ in schema.items()]))

def find_cycles(schema):
    cycles = set()
    for (t0, fields0) in schema.items():
        fields0 = set(map(lambda f: f[1][0], fields0.items()))
        for (t1, fields1) in schema.items():
            if (t0 != t1):
                fields1 = set(map(lambda f: f[1][0], fields1.items()))
                if (t0 in fields1 and t1 in fields0):
                    cycles.add((t0, t1))
    return(cycles)

if (__name__ == "__main__"):
    schema = map_schema(introspect("https://sandbox.xerpa.com.br"))
    cycles = find_cycles(schema)
    print(format_schema(schema, cycles))
